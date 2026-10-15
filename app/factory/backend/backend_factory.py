from pathlib import Path
from deepagents.backends import BackendProtocol

from app.factory.base_factory import BaseFactory
from app.factory.backend.windows_sandbox import WindowsCompatibleBackend
from app.factory.backend.linux_sandbox import LocalShellFilesystemBackend
from app.factory.backend.remote_docker_sandbox import (
    RemoteDockerSandbox,
    RemoteDockerSandboxConfig,
)
from app.config.settings import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class BackendFactory(BaseFactory):
    """Backend 工厂。"""
    def create(self, *, name: str | None = None, user_dir:str) -> BackendProtocol | None:
        # 当前示例默认不创建 backend；
        rootdir = Path()
        if settings.BACKEND_DIR:
            rootdir = Path(settings.BACKEND_DIR or (BASE_DIR + "/workspace")).resolve()
            rootdir.mkdir(parents=True, exist_ok=True)
        
        if name == "linux_filesystem_shell":
            backend = LocalShellFilesystemBackend(
                root_dir=f"{rootdir}/{user_dir}", 
                virtual_mode=True
            )
            return backend
        elif name == "windows_filesystem_shell":
            backend = WindowsCompatibleBackend(root_dir=f"{rootdir}/{user_dir}")
            # return FilesystemMiddleware(backend=backend)
            return backend
        elif name == "remote_docker_sanbox":
            config = RemoteDockerSandboxConfig(
                image_name="python:3.12-slim",
                work_dir="/workspace",
                pull_image=True,
                network_disabled=True,
            )
            return RemoteDockerSandbox(config=config)
        else:
            return None