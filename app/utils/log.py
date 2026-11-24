import sys
from pathlib import Path
from datetime import date

from loguru import logger as loguru_logger
from app.config.settings import BASE_DIR, settings

__all__ = ["logger"]


def _console_sink():
    """控制台输出流。

    Windows 控制台默认是 cp936，直接输出中文/emoji 会抛 UnicodeEncodeError，
    这里尽量把 stderr 切成 utf-8；切不动（不是 TextIOWrapper 等）就退回原流。
    """
    stream = sys.stderr
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    return stream


class LoguruLoggerManager:
    """Loguru日志管理器"""

    def __init__(self):
        self.logger = loguru_logger
        self.LONG_LOG_LIMIT = 5000
        self._configure_logger()

    def set_file_name(self, description: str):
        today = date.today()
        str_date = f"{today.year}_{today.month:02d}_{today.day:02d}_{description}"
        return str_date

    def _configure_logger(self):
        """配置loguru日志器"""
        # 移除默认的handler
        self.logger.remove()

        # 确保日志目录存在；相对路径以项目根目录为基准，避免受启动时 CWD 影响
        log_dir = Path(settings.LOG_DIR or "logs")
        if not log_dir.is_absolute():
            log_dir = BASE_DIR / log_dir
        log_dir.mkdir(parents=True, exist_ok=True)

        access_log_dir = log_dir / "access"
        access_log_dir.mkdir(parents=True, exist_ok=True)

        error_log_dir = log_dir / "error"
        error_log_dir.mkdir(parents=True, exist_ok=True)
        # 控制台输出 - 彩色格式
        color_format = (
            "<yellow>{app_id}</yellow> | "
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <4}</level> | "
            "<yellow>{name}</yellow>:<yellow>{function}</yellow>:<yellow>{line}</yellow> | "
            "<level>{message:." + str(self.LONG_LOG_LIMIT) + "}</level>\n"
        )

        plain_format = (
            "{app_id} | "
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message:." + str(self.LONG_LOG_LIMIT) + "}"
        )

        # 用 patcher 全局注入 app_id：{app_id} 是格式化串里的占位符，
        # 只要某个 sink 忘了挂 all_log_filter，就会在 emit 时抛 KeyError: 'app_id'
        # 并吞掉整条日志。放这里统一注入，新加 sink 不会踩这个坑。
        self.logger.configure(patcher=self._add_trace_context)

        # 控制台输出：loguru 自带的 stderr handler 已被上面的 remove() 移除，
        # 必须在这里显式补回来，否则服务端出错时控制台一条日志都看不到，
        # 只能去 logs/ 目录翻文件（排查 500 时非常致命）。
        self.logger.add(
            _console_sink(),
            format=color_format,
            level=settings.LOG_CONSOLE_LEVEL,
            colorize=None,
            backtrace=True,
            diagnose=settings.LOG_DIAGNOSE,
        )

        self.logger.add(
            access_log_dir / f"{self.set_file_name("debug")}.log",
            format=color_format, 
            level="DEBUG", 
            colorize=None,
            serialize=False, 
            filter=self.all_log_filter
        )

        self.logger.add(
            access_log_dir / f"{self.set_file_name("access")}.log", 
            level="INFO",
            rotation="500 MB", 
            compression="zip", 
            serialize=True,
            filter=self.all_log_filter, 
            enqueue=True, 
            encoding="utf-8",
            backtrace=True, 
            diagnose=True
        )

        self.logger.add(
            log_dir / f"{self.set_file_name("long_access")}.log", 
            level="INFO",
            format=plain_format,
            filter=self.long_log_filter, 
            enqueue=True, 
            encoding="utf-8",
            backtrace=True, 
            diagnose=True,
            rotation="500 MB", 
            compression="zip"
        )

        self.logger.add(
            error_log_dir / f"{self.set_file_name("error")}.log", 
            level="ERROR",
            rotation="500 MB", 
            compression="zip", 
            serialize=True,
            filter=self.all_log_filter, 
            enqueue=True, 
            encoding="utf-8",
            backtrace=True, 
            diagnose=True
        )

    def _add_trace_context(self, record):
        """为日志记录添加trace上下文"""
        if "app_id" not in record:
            record["app_id"] = "no-app"

    def all_log_filter(self, record):
        """判断是否为所有日志"""
        self._add_trace_context(record)
        return True

    def long_log_filter(self, record):
        """判断是否为长日志"""
        self._add_trace_context(record)
        message = record["message"]
        if len(message) > self.LONG_LOG_LIMIT:
            return True
        else:
            return False


# 初始化日志管理器
log_manager = LoguruLoggerManager()

logger = log_manager.logger
