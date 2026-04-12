# app/utils/logger.py

import logging
import logging.config
import os
from config.settings import settings


def setup_logging():
    """初始化日志系统（全局只调用一次）"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # utils/logger.py → app/utils/logger.py → 回到项目根目录

    log_dir = os.path.join(BASE_DIR, "logs")

    os.makedirs(log_dir, exist_ok=True)

    LOGGING_CONFIG = {
        "version": 1,

        # 禁止覆盖 uvicorn 默认日志（重要）
        "disable_existing_loggers": False,

        # ===== 格式 =====
        "formatters": {
            "default": {
                "format": "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
            },
            "simple": {
                "format": "%(levelname)s: %(message)s"
            },
        },

        # ===== 输出位置 =====
        "handlers": {
            # 控制台
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            },

            # 普通日志文件（自动切割）
            "file_info": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(log_dir, "info.log"),
                "when": "midnight",   # 每天切割
                "interval": 1,
                "backupCount": 7,     # 保留7天
                "encoding": "utf-8",
                "formatter": "default",
                "level": "INFO",
            },

            # 错误日志
            "file_error": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(log_dir, "error.log"),
                "when": "midnight",
                "interval": 1,
                "backupCount": 7,
                "encoding": "utf-8",
                "formatter": "default",
                "level": "ERROR",
            },
        },

        # ===== Logger定义 =====
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file_info", "file_error"],
                "level": "INFO",
            },

            # 你可以给不同模块单独定义
            "crawler": {
                "handlers": ["console", "file_info"],
                "level": "INFO",
                "propagate": False,
            },

            "ai": {
                "handlers": ["console", "file_info"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name: str):
    """获取logger"""
    return logging.getLogger(name)