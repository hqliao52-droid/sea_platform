import subprocess
import sys
from pathlib import Path

import uvicorn

from app.config.settings import settings

ROOT_DIR = Path(__file__).resolve().parent
_children: list[subprocess.Popen] = []


def _start(name: str, cmd: list[str]) -> None:
    proc = subprocess.Popen(cmd, cwd=ROOT_DIR)
    _children.append(proc)
    print(f"[main] {name} 已启动 (pid={proc.pid})")


def start_background_workers() -> None:
    python = sys.executable

    _start(
        "rss-worker",
        [python, str(ROOT_DIR / "worker" / "rss_result_execute_worker.py")],
    )

    celery_cmd = [
        python, "-m", "celery",
        "-A", "app.tasks.celery_app",
        "worker", "-l", "info",
    ]
    if sys.platform == "win32":
        celery_cmd.append("--pool=solo")   # Windows 没有 fork，prefork 池不可用
    _start("celery-worker", celery_cmd)


def stop_background_workers() -> None:
    for proc in _children:
        if proc.poll() is None:
            proc.terminate()
    for proc in _children:
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
    _children.clear()


if __name__ == "__main__":
    # start_background_workers()
    try:
        uvicorn.run(
            app="app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=(True if settings.DEBUG else False),
        )
    finally:
        stop_background_workers()