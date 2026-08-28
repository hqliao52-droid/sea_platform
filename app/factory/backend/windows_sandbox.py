"""Windows-compatible filesystem + execution backend for DeepAgents.

Implements `deepagents.backends.protocol.BackendProtocol` and
`SandboxBackendProtocol` so it can be passed directly to `FilesystemMiddleware`
(or `create_deep_agent(backend=...)`) and just work on Windows.

Why a dedicated backend:
- DeepAgents' built-in `execute` tool description assumes POSIX tools
  (`find`, `grep`, `cat`, `&&`/`;` shell semantics) and `FilesystemBackend`
  assumes POSIX-style absolute paths. On Windows, drive letters (`C:\\`),
  backslashes, `cmd.exe`/PowerShell quoting, and the absence of `find`/`grep`
  by default break both file ops and the execute tool.
- This backend maps the agent's virtual POSIX-style paths (always starting
  with `/`) onto a real Windows (or POSIX) root directory, and runs shell
  commands through the correct platform shell automatically.

Usage:
    from backend import WindowsCompatibleBackend
    from deepagents.middleware.filesystem import FilesystemMiddleware
    from langchain.agents import create_agent

    backend = WindowsCompatibleBackend(root_dir=r"C:\\agent-workspace")

    agent = create_agent(
        model="anthropic:claude-sonnet-4-6",
        middleware=[FilesystemMiddleware(backend=backend)],
    )

Or with create_deep_agent:
    from deepagents import create_deep_agent
    agent = create_deep_agent(backend=WindowsCompatibleBackend(root_dir="./workspace"))
"""

from __future__ import annotations

import fnmatch
import os
import platform
import shutil
import subprocess
import sys
import threading
import time
import uuid
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath

from deepagents.backends.protocol import (
    EditResult,
    ExecuteResponse,
    FileData,
    FileDownloadResponse,
    FileInfo,
    FileUploadResponse,
    GlobResult,
    GrepMatch,
    GrepResult,
    LsResult,
    ReadResult,
    SandboxBackendProtocol,
    WriteResult,
)

IS_WINDOWS = platform.system() == "Windows" or os.name == "nt"

MAX_LINE_LENGTH = 2000

BINARY_EXTENSIONS = {".pptx", ".docx", ".xlsx", ".pdf", ".png", ".jpg", ".jpeg", ".zip"}

# Windows 盘符路径 (C:\, D:/ 等)，UNC 路径 (\\server\share)，POSIX 绝对路径
_ABS_PATH_PATTERN = re.compile(
    r"(?:^|[\s\"'(&|])"          # 前面是命令开头/空格/引号/括号/管道等分隔符
    r"(?:[A-Za-z]:[\\/]|\\\\[^\\]+\\|/(?!\s|$))"
)
_CD_ESCAPE_PATTERN = re.compile(
    r"\bcd\s+(?:/d\s+)?(?:[A-Za-z]:|\\\\|\.\.[\\/]|/)", re.IGNORECASE
)

class WorkdirEscapeError(ValueError):
    """Raised when a command attempts to access paths outside root_dir."""

def _check_command_escape(command: str) -> str | None:
    """Return an error message if the command looks like it escapes root_dir, else None."""
    if _ABS_PATH_PATTERN.search(command):
        return (
            "Command rejected: absolute paths (e.g. C:\\..., \\\\server\\..., "
            "or POSIX /...) are not allowed. This sandbox's working directory "
            "already IS your filesystem root — use relative paths or filenames "
            "directly (e.g. `python check_env.py`, not `python C:\\...\\check_env.py`)."
        )
    if _CD_ESCAPE_PATTERN.search(command):
        return (
            "Command rejected: changing directory outside the sandbox root "
            "(e.g. `cd ..`, `cd C:\\`) is not allowed. Stay within the current "
            "working directory; all your files are already here."
        )
    return None

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class PathSecurityError(ValueError):
    """Raised when a resolved path would escape the backend's root_dir."""


class WindowsCompatibleBackend(SandboxBackendProtocol):
    """Local-disk backend with Windows-safe path handling and shell execution.

    Agent-facing paths are always POSIX-style and must start with `/`
    (e.g. `/src/main.py`). They are mapped onto `root_dir` on the real
    filesystem, working correctly whether `root_dir` is a Windows path
    (`C:\\agent-workspace`) or a POSIX path (`/home/user/workspace`).

    Args:
        root_dir: Real filesystem directory all virtual paths resolve under.
            Created if it doesn't exist. Defaults to a temp-like local
            `./deepagents-workspace` directory.
        shell: Force a shell mode instead of auto-detecting. One of
            "cmd", "powershell", "posix", or None (auto-detect by platform).
        default_timeout: Default `execute` timeout in seconds.
        env: Extra environment variables merged into the subprocess env.
    """

    def __init__(
        self,
        root_dir: str | os.PathLike[str] | None = None,
        *,
        shell: str | None = None,
        default_timeout: int = 120,
        env: dict[str, str] | None = None,
    ) -> None:
        self.root_dir = Path(root_dir or "./deepagents-workspace").resolve()
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self._shell = shell or ("cmd" if IS_WINDOWS else "posix")
        self._default_timeout = default_timeout
        self._extra_env = env or {}
        self._id = f"windows-backend-{uuid.uuid4().hex[:8]}"

    # ------------------------------------------------------------------
    # Path handling
    # ------------------------------------------------------------------

    def _to_real_path(self, virtual_path: str) -> Path:
        """Map a virtual POSIX-style path (must start with '/') to a real path."""
        if not virtual_path.startswith("/"):
            msg = f"Path must be absolute (start with '/'): {virtual_path!r}"
            raise PathSecurityError(msg)

        # Strip leading slash, normalize any accidental backslashes from the
        # model (it may have learned Windows habits), then split into parts.
        cleaned = virtual_path.lstrip("/").replace("\\", "/")
        parts = [p for p in cleaned.split("/") if p not in ("", ".")]

        real = self.root_dir
        for part in parts:
            if part == "..":
                msg = f"Path traversal is not allowed: {virtual_path!r}"
                raise PathSecurityError(msg)
            real = real / part

        real_resolved = real.resolve() if real.exists() else real
        # Defense in depth: ensure final path stays under root_dir even
        # after symlink resolution.
        try:
            real_resolved.relative_to(self.root_dir.resolve())
        except ValueError as exc:
            msg = f"Resolved path escapes root_dir: {virtual_path!r}"
            raise PathSecurityError(msg) from exc
        return real

    def _to_virtual_path(self, real_path: Path) -> str:
        rel = real_path.resolve().relative_to(self.root_dir.resolve())
        # PureWindowsPath -> posix string works whether we're on Windows or not
        posix = PureWindowsPath(rel).as_posix() if IS_WINDOWS else rel.as_posix()
        return "/" + posix if posix != "." else "/"

    # ------------------------------------------------------------------
    # BackendProtocol: ls
    # ------------------------------------------------------------------

    def ls(self, path: str) -> LsResult:
        try:
            real = self._to_real_path(path)
        except PathSecurityError as exc:
            return LsResult(error=str(exc))

        if not real.exists():
            return LsResult(error=f"Path not found: {path}")
        if not real.is_dir():
            return LsResult(error=f"Not a directory: {path}")

        entries: list[FileInfo] = []
        try:
            for child in sorted(real.iterdir()):
                stat = child.stat()
                info: FileInfo = {
                    "path": self._to_virtual_path(child),
                    "is_dir": child.is_dir(),
                    "size": stat.st_size,
                    "modified_at": datetime.fromtimestamp(
                        stat.st_mtime, tz=timezone.utc
                    ).isoformat(),
                }
                entries.append(info)
        except OSError as exc:
            return LsResult(error=f"Failed to list directory: {exc}")
        return LsResult(entries=entries)

    # ------------------------------------------------------------------
    # BackendProtocol: read
    # ------------------------------------------------------------------

    def read(self, file_path: str, offset: int = 0, limit: int = 2000) -> ReadResult:
        try:
            real = self._to_real_path(file_path)
        except PathSecurityError as exc:
            return ReadResult(error=str(exc))

        if not real.exists():
            return ReadResult(error=f"File not found: {file_path}")
        if real.is_dir():
            return ReadResult(error=f"Path is a directory, not a file: {file_path}")

        if real.suffix.lower() in BINARY_EXTENSIONS:
            return ReadResult(
                error=(
                    f"{file_path} is a binary file ({real.suffix}) and cannot be read as text. "
                    f"Use the execute tool to run a Python script that processes it "
                    f"(e.g. python-pptx for .pptx files), instead of calling read on it directly."
                )
            )
        try:
            raw_bytes = real.read_bytes()
        except OSError as exc:
            return ReadResult(error=f"Failed to read file: {exc}")
        if b"\x00" in raw_bytes[:8192]:
            return ReadResult(
                error=(
                    f"{file_path} appears to be a binary file and cannot be read as text. "
                    f"Use the execute tool to process it with an appropriate library instead."
                )
            )
        
        try:
            raw = real.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            return ReadResult(error=f"Failed to read file: {exc}")

        lines = raw.splitlines()
        stat = real.stat()
        file_data: FileData = {
            "content": raw,
            "encoding": "utf-8",
            "created_at": datetime.fromtimestamp(
                stat.st_ctime, tz=timezone.utc
            ).isoformat(),
            "modified_at": datetime.fromtimestamp(
                stat.st_mtime, tz=timezone.utc
            ).isoformat(),
        }
        # Slice for offset/limit, matching the "cat -n" style expectation.
        selected = lines[offset : offset + limit]
        truncated_lines = [
            (line[: MAX_LINE_LENGTH - 3] + "...") if len(line) > MAX_LINE_LENGTH else line
            for line in selected
        ]
        file_data["content"] = "\n".join(
            f"{i + offset + 1:>6}\t{line}" for i, line in enumerate(truncated_lines)
        )
        return ReadResult(file_data=file_data)

    # ------------------------------------------------------------------
    # BackendProtocol: write
    # ------------------------------------------------------------------

    def write(self, file_path: str, content: str) -> WriteResult:
        try:
            real = self._to_real_path(file_path)
        except PathSecurityError as exc:
            return WriteResult(error=str(exc))

        if real.exists():
            return WriteResult(error=f"File already exists: {file_path}")

        try:
            real.parent.mkdir(parents=True, exist_ok=True)
            real.write_text(content, encoding="utf-8", newline="\n")
        except OSError as exc:
            return WriteResult(error=f"Failed to write file: {exc}")
        return WriteResult(path=file_path)

    # ------------------------------------------------------------------
    # BackendProtocol: edit
    # ------------------------------------------------------------------

    def edit(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        replace_all: bool = False,
    ) -> EditResult:
        try:
            real = self._to_real_path(file_path)
        except PathSecurityError as exc:
            return EditResult(error=str(exc))

        if not real.exists():
            return EditResult(error=f"File not found: {file_path}")

        try:
            text = real.read_text(encoding="utf-8")
        except OSError as exc:
            return EditResult(error=f"Failed to read file: {exc}")

        count = text.count(old_string)
        if count == 0:
            return EditResult(error=f"String not found in file: {old_string!r}")
        if count > 1 and not replace_all:
            return EditResult(
                error=(
                    f"String is not unique in file ({count} occurrences). "
                    "Use replace_all=True or provide more context."
                )
            )

        new_text = text.replace(old_string, new_string) if replace_all else text.replace(
            old_string, new_string, 1
        )
        occurrences = count if replace_all else 1

        try:
            real.write_text(new_text, encoding="utf-8", newline="\n")
        except OSError as exc:
            return EditResult(error=f"Failed to write file: {exc}")

        return EditResult(path=file_path, occurrences=occurrences)

    # ------------------------------------------------------------------
    # BackendProtocol: glob
    # ------------------------------------------------------------------

    def glob(self, pattern: str, path: str = "/") -> GlobResult:
        try:
            real_base = self._to_real_path(path)
        except PathSecurityError as exc:
            return GlobResult(error=str(exc))

        if not real_base.exists():
            return GlobResult(error=f"Path not found: {path}")

        try:
            matches = sorted(real_base.glob(pattern))
        except (OSError, ValueError) as exc:
            return GlobResult(error=f"Invalid glob pattern: {exc}")

        results: list[FileInfo] = []
        for m in matches:
            try:
                stat = m.stat()
            except OSError:
                continue
            results.append(
                {
                    "path": self._to_virtual_path(m),
                    "is_dir": m.is_dir(),
                    "size": stat.st_size,
                    "modified_at": datetime.fromtimestamp(
                        stat.st_mtime, tz=timezone.utc
                    ).isoformat(),
                }
            )
        return GlobResult(matches=results)

    # ------------------------------------------------------------------
    # BackendProtocol: grep (pure-Python, no dependency on `grep`/`findstr`)
    # ------------------------------------------------------------------

    def grep(
        self,
        pattern: str,
        path: str | None = None,
        glob: str | None = None,
    ) -> GrepResult:
        try:
            real_base = self._to_real_path(path) if path else self.root_dir
        except PathSecurityError as exc:
            return GrepResult(error=str(exc))

        if not real_base.exists():
            return GrepResult(error=f"Path not found: {path}")

        files: list[Path]
        if real_base.is_file():
            files = [real_base]
        else:
            files = [p for p in real_base.rglob("*") if p.is_file()]
            if glob:
                files = [p for p in files if fnmatch.fnmatch(p.name, glob) or fnmatch.fnmatch(
                    self._to_virtual_path(p).lstrip("/"), glob
                )]

        matches: list[GrepMatch] = []
        for f in files:
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if pattern in line:
                    matches.append(
                        {
                            "path": self._to_virtual_path(f),
                            "line": line_no,
                            "text": line[:MAX_LINE_LENGTH],
                        }
                    )
        return GrepResult(matches=matches)

    # ------------------------------------------------------------------
    # BackendProtocol: upload/download
    # ------------------------------------------------------------------

    def upload_files(self, files: list[tuple[str, bytes]]) -> list[FileUploadResponse]:
        responses: list[FileUploadResponse] = []
        for path, content in files:
            try:
                real = self._to_real_path(path)
            except PathSecurityError:
                responses.append(FileUploadResponse(path=path, error="invalid_path"))
                continue
            try:
                real.parent.mkdir(parents=True, exist_ok=True)
                real.write_bytes(content)
                responses.append(FileUploadResponse(path=path))
            except PermissionError:
                responses.append(FileUploadResponse(path=path, error="permission_denied"))
            except OSError as exc:
                responses.append(FileUploadResponse(path=path, error=str(exc)))
        return responses

    def download_files(self, paths: list[str]) -> list[FileDownloadResponse]:
        responses: list[FileDownloadResponse] = []
        for path in paths:
            try:
                real = self._to_real_path(path)
            except PathSecurityError:
                responses.append(FileDownloadResponse(path=path, error="invalid_path"))
                continue
            if not real.exists():
                responses.append(FileDownloadResponse(path=path, error="file_not_found"))
                continue
            if real.is_dir():
                responses.append(FileDownloadResponse(path=path, error="is_directory"))
                continue
            try:
                responses.append(
                    FileDownloadResponse(path=path, content=real.read_bytes())
                )
            except PermissionError:
                responses.append(FileDownloadResponse(path=path, error="permission_denied"))
            except OSError as exc:
                responses.append(FileDownloadResponse(path=path, error=str(exc)))
        return responses

    # ------------------------------------------------------------------
    # SandboxBackendProtocol: execute
    # ------------------------------------------------------------------

    @property
    def id(self) -> str:
        return self._id

    def _build_subprocess_args(self, command: str) -> tuple[list[str] | str, bool]:
        """Return (args, use_shell) for subprocess.run based on `self._shell`."""
        if self._shell == "cmd":
            # /d: ignore AutoRun, /s: strip quotes correctly, /c: run then exit
            return (["cmd.exe", "/d", "/s", "/c", command], False)
        if self._shell == "powershell":
            exe = shutil.which("pwsh") or "powershell.exe"
            return ([exe, "-NoProfile", "-NonInteractive", "-Command", command], False)
        # posix: use the system shell (bash/sh) directly
        return (command, True)

    def _output_encoding(self) -> str:
        """Pick the right encoding to decode subprocess output with.

        - `cmd.exe` on a Chinese (or other non-UTF8) Windows install writes
          output in the system's active OEM/ANSI code page (commonly CP936 /
          GBK), NOT UTF-8. Decoding that as UTF-8 produces mojibake.
        - PowerShell (modern `pwsh`/Windows PowerShell with `$OutputEncoding`
          unset) is more consistent but still console-codepage dependent in
          many setups.
        - POSIX shells are UTF-8 in virtually all modern environments.
        """
        if self._shell == "posix":
            return "utf-8"
        # On Windows, ask the OS for its actual console/ANSI codepage encoding
        # instead of assuming UTF-8. `locale.getpreferredencoding()` reflects
        # the active code page (e.g. 'cp936' on zh-CN Windows, 'cp1252' on
        # US/EU Windows) and matches what cmd.exe / legacy PowerShell emit.
        import locale

        return locale.getpreferredencoding(do_setlocale=False) or "mbcs"

    def execute(self, command: str, *, timeout: int | None = None) -> ExecuteResponse:
        escape_error = _check_command_escape(command)
        if escape_error is not None:
            return ExecuteResponse(output=escape_error, exit_code=1)

        effective_timeout = timeout if timeout is not None else self._default_timeout
        use_timeout = None if effective_timeout == 0 else effective_timeout

        args, use_shell = self._build_subprocess_args(command)
        env = {**os.environ, **self._extra_env}
        out_encoding = self._output_encoding()

        try:
            completed = subprocess.run(  # noqa: S602 (shell content is the agent's own command, by design)
                args,
                shell=use_shell,
                cwd=str(self.root_dir),
                env=env,
                capture_output=True,
                # Capture raw bytes ourselves instead of letting subprocess
                # decode with a hardcoded/guessed encoding, so we can apply
                # the correct platform-specific codepage below.
                text=False,
                timeout=use_timeout,
            )
        except subprocess.TimeoutExpired as exc:
            partial_bytes = (exc.stdout or b"") + (exc.stderr or b"")
            partial = partial_bytes.decode(out_encoding, errors="replace")
            return ExecuteResponse(
                output=f"{partial}\n[Command timed out after {effective_timeout}s]",
                exit_code=None,
                truncated=True,
            )
        except FileNotFoundError as exc:
            return ExecuteResponse(
                output=f"Shell executable not found: {exc}",
                exit_code=127,
            )
        except OSError as exc:
            return ExecuteResponse(output=f"Execution error: {exc}", exit_code=1)

        raw_output = (completed.stdout or b"") + (completed.stderr or b"")
        output = raw_output.decode(out_encoding, errors="replace")
        truncated = False
        max_output = 50_000
        if len(output) > max_output:
            output = output[:max_output] + "\n[Output truncated]"
            truncated = True

        return ExecuteResponse(
            output=output,
            exit_code=completed.returncode,
            truncated=truncated,
        )

    async def aexecute(
        self, command: str, *, timeout: int | None = None
    ) -> ExecuteResponse:
        import asyncio

        return await asyncio.to_thread(self.execute, command, timeout=timeout)