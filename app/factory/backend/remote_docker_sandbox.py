# from __future__ import annotations

# import io
# import posixpath
# import shlex
# import tarfile
# import uuid
# from dataclasses import dataclass, field
# from typing import Any, Mapping

# from deepagents.backends.protocol import (
#     ExecuteResponse,
#     FileDownloadResponse,
#     FileUploadResponse,
# )
# from deepagents.backends.sandbox import BaseSandbox
# from docker import DockerClient


# @dataclass(slots=True)
# class RemoteDockerSandboxConfig:
#     """远程 Docker 沙盒配置。"""

#     base_url: str | None = None
#     image: str = "python:3.12-slim"
#     name_prefix: str = "deepagents-sandbox"
#     workdir: str = "/workspace"

#     default_timeout: int = 30 * 60
#     docker_api_timeout: int = 60
#     max_output_bytes: int = 1024 * 1024

#     pull_image: bool = False
#     remove_on_close: bool = True

#     network_disabled: bool = True
#     mem_limit: str = "1g"
#     nano_cpus: int = 1_000_000_000
#     pids_limit: int = 256

#     read_only: bool = False
#     cap_drop: list[str] = field(default_factory=lambda: ["ALL"])
#     security_opt: list[str] = field(default_factory=lambda: ["no-new-privileges:true"])

#     environment: Mapping[str, str] = field(default_factory=dict)
#     labels: Mapping[str, str] = field(
#         default_factory=lambda: {"deepagents.sandbox": "true"}
#     )


# class RemoteDockerSandbox(BaseSandbox):
#     """基于远程 Docker Engine 的 DeepAgents `BaseSandbox` 实现。

#     一个 sandbox 对应一个长期运行容器。`BaseSandbox` 继承来的
#     `read/write/edit/ls/grep/glob` 会基于这里实现的 `execute`、
#     `upload_files` 和 `download_files` 自动可用。
#     """

#     def __init__(
#         self,
#         config: RemoteDockerSandboxConfig | None = None,
#         *,
#         container_id: str | None = None,
#         docker_client: DockerClient | None = None,
#     ) -> None:
#         self.config = config or RemoteDockerSandboxConfig()
#         self._client: DockerClient = docker_client or self._create_client(self.config)
#         self._owns_container = container_id is None

#         if container_id:
#             self._container = self._client.containers.get(container_id)
#         else:
#             self._container = self._create_container()

#     @property
#     def id(self) -> str:
#         """返回底层 Docker container id。"""
#         return self._container.id

#     def execute(
#         self,
#         command: str,
#         *,
#         timeout: int | None = None,
#     ) -> ExecuteResponse:
#         """在远程 Docker 容器内执行 shell command。"""
#         effective_timeout = (
#             self.config.default_timeout if timeout is None else int(timeout)
#         )

#         if effective_timeout > 0:
#             wrapped = (
#                 f"timeout --kill-after=5s {effective_timeout}s "
#                 f"/bin/sh -lc {shlex.quote(command)}"
#             )
#         else:
#             wrapped = f"/bin/sh -lc {shlex.quote(command)}"

#         try:
#             result = self._container.exec_run(
#                 cmd=["/bin/sh", "-lc", wrapped],
#                 stdout=True,
#                 stderr=True,
#                 demux=False,
#                 workdir=self.config.workdir,
#                 tty=False,
#             )
#         except Exception as exc:
#             return ExecuteResponse(
#                 output=f"Docker execution error: {exc}",
#                 exit_code=1,
#                 truncated=False,
#             )

#         raw_output = result.output or b""
#         truncated = False
#         if len(raw_output) > self.config.max_output_bytes:
#             raw_output = raw_output[: self.config.max_output_bytes]
#             truncated = True

#         output = raw_output.decode("utf-8", errors="replace")
#         if truncated:
#             output += (
#                 "\n\n[Output was truncated by RemoteDockerSandbox "
#                 f"at {self.config.max_output_bytes} bytes.]"
#             )

#         return ExecuteResponse(
#             output=output,
#             exit_code=int(result.exit_code) if result.exit_code is not None else None,
#             truncated=truncated,
#         )

#     def upload_files(
#         self,
#         files: list[tuple[str, bytes]],
#     ) -> list[FileUploadResponse]:
#         """上传多个文件到容器。"""
#         responses: list[FileUploadResponse] = []

#         for path, content in files:
#             if not self._is_abs_path(path) or path.endswith("/"):
#                 responses.append(FileUploadResponse(path=path, error="invalid_path"))
#                 continue

#             parent = posixpath.dirname(path) or "/"
#             filename = posixpath.basename(path)
#             mkdir_result = self.execute(f"mkdir -p {shlex.quote(parent)}")
#             if mkdir_result.exit_code != 0:
#                 responses.append(
#                     FileUploadResponse(path=path, error="permission_denied")
#                 )
#                 continue

#             try:
#                 tar_data = self._build_single_file_tar(filename, content)
#                 ok = self._container.put_archive(parent, tar_data)
#                 error = None if ok else "permission_denied"
#                 responses.append(FileUploadResponse(path=path, error=error))
#             except Exception:
#                 responses.append(
#                     FileUploadResponse(path=path, error="permission_denied")
#                 )

#         return responses

#     def download_files(
#         self,
#         paths: list[str],
#     ) -> list[FileDownloadResponse]:
#         """从容器下载多个文件。"""
#         responses: list[FileDownloadResponse] = []

#         for path in paths:
#             if not self._is_abs_path(path):
#                 responses.append(
#                     FileDownloadResponse(path=path, content=None, error="invalid_path")
#                 )
#                 continue

#             check = self.execute(
#                 "python3 - <<'PY'\n"
#                 "import os, sys\n"
#                 f"path = {path!r}\n"
#                 "if not os.path.exists(path): sys.exit(44)\n"
#                 "if os.path.isdir(path): sys.exit(45)\n"
#                 "if not os.access(path, os.R_OK): sys.exit(46)\n"
#                 "sys.exit(0)\n"
#                 "PY"
#             )

#             if check.exit_code == 44:
#                 responses.append(
#                     FileDownloadResponse(
#                         path=path,
#                         content=None,
#                         error="file_not_found",
#                     )
#                 )
#                 continue
#             if check.exit_code == 45:
#                 responses.append(
#                     FileDownloadResponse(path=path, content=None, error="is_directory")
#                 )
#                 continue
#             if check.exit_code not in (0, None):
#                 responses.append(
#                     FileDownloadResponse(
#                         path=path,
#                         content=None,
#                         error="permission_denied",
#                     )
#                 )
#                 continue

#             try:
#                 stream, _stat = self._container.get_archive(path)
#                 tar_bytes = b"".join(stream)
#                 content = self._extract_first_regular_file(tar_bytes)
#                 responses.append(
#                     FileDownloadResponse(path=path, content=content, error=None)
#                 )
#             except IsADirectoryError:
#                 responses.append(
#                     FileDownloadResponse(path=path, content=None, error="is_directory")
#                 )
#             except FileNotFoundError:
#                 responses.append(
#                     FileDownloadResponse(
#                         path=path,
#                         content=None,
#                         error="file_not_found",
#                     )
#                 )
#             except Exception as exc:
#                 responses.append(
#                     FileDownloadResponse(
#                         path=path,
#                         content=None,
#                         error=f"download_error: {exc}",
#                     )
#                 )

#         return responses

#     def close(self) -> None:
#         """停止并删除沙盒容器。"""
#         if not self._owns_container or not self.config.remove_on_close:
#             return

#         try:
#             self._container.remove(force=True)
#         except Exception:
#             pass

#     def __enter__(self) -> RemoteDockerSandbox:
#         return self

#     def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
#         self.close()

#     @staticmethod
#     def _create_client(config: RemoteDockerSandboxConfig) -> DockerClient:
#         try:
#             import docker
#         except ImportError as exc:
#             raise RuntimeError(
#                 "RemoteDockerSandbox requires the Docker SDK for Python. "
#                 "Install project dependencies before enabling `remote_docker`."
#             ) from exc

#         return docker.DockerClient(
#             base_url=config.base_url or "unix://var/run/docker.sock",
#             version="auto",
#             timeout=config.docker_api_timeout,
#         )

#     def _create_container(self) -> Any:
#         if self.config.pull_image:
#             self._client.images.pull(self.config.image)

#         name = f"{self.config.name_prefix}-{uuid.uuid4().hex[:12]}"
#         try:
#             return self._client.containers.run(
#                 image=self.config.image,
#                 command=[
#                     "/bin/sh",
#                     "-lc",
#                     f"mkdir -p {shlex.quote(self.config.workdir)} && sleep infinity",
#                 ],
#                 name=name,
#                 detach=True,
#                 working_dir="/",
#                 environment=dict(self.config.environment),
#                 labels=dict(self.config.labels),
#                 network_disabled=self.config.network_disabled,
#                 mem_limit=self.config.mem_limit,
#                 nano_cpus=self.config.nano_cpus,
#                 pids_limit=self.config.pids_limit,
#                 read_only=self.config.read_only,
#                 cap_drop=self.config.cap_drop,
#                 security_opt=self.config.security_opt,
#                 auto_remove=False,
#             )
#         except Exception as exc:
#             raise RuntimeError(
#                 f"Failed to create remote Docker sandbox: {exc}"
#             ) from exc

#     @staticmethod
#     def _is_abs_path(path: str) -> bool:
#         return isinstance(path, str) and path.startswith("/") and "\x00" not in path

#     @staticmethod
#     def _build_single_file_tar(filename: str, content: bytes) -> bytes:
#         fileobj = io.BytesIO()
#         with tarfile.open(fileobj=fileobj, mode="w") as tar:
#             info = tarfile.TarInfo(name=filename)
#             info.size = len(content)
#             info.mode = 0o644
#             tar.addfile(info, io.BytesIO(content))
#         fileobj.seek(0)
#         return fileobj.getvalue()

#     @staticmethod
#     def _extract_first_regular_file(tar_bytes: bytes) -> bytes:
#         with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:*") as tar:
#             for member in tar.getmembers():
#                 if member.isdir():
#                     raise IsADirectoryError(member.name)
#                 if member.isfile():
#                     extracted = tar.extractfile(member)
#                     return extracted.read() if extracted is not None else b""
#         raise FileNotFoundError("No regular file found in tar archive")
