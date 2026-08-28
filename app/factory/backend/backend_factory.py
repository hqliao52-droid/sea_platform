from pathlib import Path
from deepagents.backends import BackendProtocol

from app.factory.base_factory import BaseFactory
from app.factory.backend.windows_sandbox import WindowsCompatibleBackend
from app.factory.backend.linux_sandbox import LocalShellFilesystemBackend
from app.config.settings import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class BackendFactory(BaseFactory):
    """Backend 工厂。"""
    def create(self, *, name: str | None = None, user_dir:str) -> BackendProtocol | None:
        if not name:
            return None
        # 当前示例默认不创建 backend；
        if settings.BACKEND_DIR:
            rootdir = Path(settings.BACKEND_DIR or (BASE_DIR + "/workspace")).resolve()
            rootdir.mkdir(parents=True, exist_ok=True)
        if name == "windows_filesystem_shell":
            backend = WindowsCompatibleBackend(f"{rootdir}/{user_dir}")
            # return FilesystemMiddleware(backend=backend)
            return backend
        elif name == "linux_filesystem_shell":
            backend = LocalShellFilesystemBackend(f"{rootdir}/{user_dir}")
            return backend
        return None