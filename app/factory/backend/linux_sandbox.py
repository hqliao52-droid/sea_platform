from deepagents.backends import LocalShellBackend
from pathlib import Path


import os
import re


from deepagents.backends.protocol import (
    EditResult,
    GrepMatch,
    WriteResult,
)
from deepagents.backends.utils import (
    perform_string_replacement,
)


class LocalShellFilesystemBackend(LocalShellBackend):
    """ Shell 文件系统后端。"""

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        """初始化文件系统后端。"""
        # 传递当前进程的环境变量，windows、linux补丁
        kwargs["env"] = os.environ.copy()
        super().__init__(*args, **kwargs)

    def _resolve_path(self, key: str) -> Path:

        if self.virtual_mode:
            vpath = key if key.startswith("/") else "/" + key
            if vpath.startswith("/workspace/"):
                vpath = vpath[len("/workspace") :]
            try:
                # 支持传入完整的绝对路径
                full = Path(vpath).resolve()
                rel = full.relative_to(self.cwd)
                vpath = str(rel)
                vpath = vpath if vpath.startswith("/") else "/" + vpath
            except ValueError:
                pass

            if ".." in vpath or vpath.startswith("~"):
                msg = "Path traversal not allowed"
                raise ValueError(msg)
            full = (self.cwd / vpath.lstrip("/")).resolve()
            try:
                full.relative_to(self.cwd)
            except ValueError:
                msg = f"Path:{full} outside root directory: {self.cwd}"
                raise ValueError(msg) from None
            return full

        path = Path(key)
        if path.is_absolute():
            return path
        return (self.cwd / path).resolve()

    def write(
        self,
        file_path: str,
        content: str,
    ) -> WriteResult:
        """Create a new file with content.

        Args:
            file_path: Path where the new file will be created.
            content: Text content to write to the file.

        Returns:
            `WriteResult` with path on success, or error message if the file
                already exists or write fails. External storage sets `files_update=None`.
        """
        resolved_path = self._resolve_path(file_path)
        _file_path = str(resolved_path)

        if resolved_path.exists():
            return WriteResult(
                error=f"Cannot write to {_file_path} because it already exists. Read and then make an edit, or write to a new path."
            )

        try:
            # Create parent directories if needed
            resolved_path.parent.mkdir(parents=True, exist_ok=True)

            # Prefer O_NOFOLLOW to avoid writing through symlinks
            flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            fd = os.open(resolved_path, flags, 0o644)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(content)

            return WriteResult(
                path=str({"file_path": _file_path}), files_update=None
            )  # use the absolute path as the path
        except (OSError, UnicodeEncodeError) as e:
            return WriteResult(error=f"Error writing file '{_file_path}': {e}")

    def grep_raw(
        self,
        pattern: str,
        path: str | None = None,
        glob: str | None = None,
    ) -> list[GrepMatch] | str:
        """Search for a literal text pattern in files.

        Uses ripgrep if available, falling back to Python search.

        Args:
            pattern: Literal string to search for (NOT regex).
            path: Directory or file path to search in. Defaults to current directory.
            glob: Optional glob pattern to filter which files to search.

        Returns:
            List of GrepMatch dicts containing path, line number, and matched text.
        """
        # Resolve base path
        try:
            base_full = self._resolve_path(path or ".")
        except ValueError:
            return []

        if not base_full.exists():
            return []

        # Try ripgrep first (with -F flag for literal search)
        results = self._ripgrep_search(pattern, base_full, glob)
        if results is None:
            # Python fallback needs escaped pattern for literal search
            results = self._python_search(re.escape(pattern), base_full, glob)

        matches: list[GrepMatch] = []
        for fpath, items in results.items():
            for line_num, line_text in items:
                matches.append(
                    {
                        "path": str(self._resolve_path(fpath)),
                        "line": int(line_num),
                        "text": line_text,
                    }
                )
        return matches

    def edit(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        replace_all: bool = False,  # noqa: FBT001, FBT002
    ) -> EditResult:
        """Edit a file by replacing string occurrences.

        Args:
            file_path: Path to the file to edit.
            old_string: The text to search for and replace.
            new_string: The replacement text.
            replace_all: If `True`, replace all occurrences. If `False` (default),
                replace only if exactly one occurrence exists.

        Returns:
            `EditResult` with path and occurrence count on success, or error
                message if file not found or replacement fails. External storage sets
                `files_update=None`.
        """
        resolved_path = self._resolve_path(file_path)
        _file_path = str(resolved_path)
        if not resolved_path.exists() or not resolved_path.is_file():
            return EditResult(error=f"Error: File '{_file_path}' not found")

        try:
            # Read securely
            fd = os.open(resolved_path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            with os.fdopen(fd, "r", encoding="utf-8") as f:
                content = f.read()

            result = perform_string_replacement(
                content, old_string, new_string, replace_all
            )

            if isinstance(result, str):
                return EditResult(error=result)

            new_content, occurrences = result

            # Write securely
            flags = os.O_WRONLY | os.O_TRUNC
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            fd = os.open(resolved_path, flags)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(new_content)

            return EditResult(
                path=str({"file_path": _file_path}),
                files_update=None,
                occurrences=int(occurrences),
            )
        except (OSError, UnicodeDecodeError, UnicodeEncodeError) as e:
            return EditResult(error=f"Error editing file '{_file_path}': {e}")
