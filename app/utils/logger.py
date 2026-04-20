import logging
import os
import signal
import sys
from datetime import date


class Logger:

    @staticmethod
    def logs_path():
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 向上两级到达 项目 目录
        pro_root = os.path.dirname(os.path.dirname(current_dir))
        # 拼接 logs 目录
        logs_dir = os.path.join(pro_root, 'logs')
        return logs_dir


    def set_file_date():
        today = date.today()
        str_date = f"{today.year}_{today.month:02d}_{today.day:02d}_log"
        return str_date
    
    def set_file_name(description:str):
        today = date.today()
        str_date = f"{today.year}_{today.month:02d}_{today.day:02d}_{description}_log"
        return str_date
    
    def set_logger_file_llm():
        today = date.today()
        str_date = f"{today.year}_{today.month:02d}_{today.day:02d}_llm"
        return str_date
    
    def setup_logger(name: str, log_file: str = None):
        logs_path = Logger.logs_path()
        os.makedirs(logs_path, exist_ok=True)

        log_file = log_file or os.path.join(logs_path, f"{name}.log")

        class DoubleNewlineFormatter(logging.Formatter):
            def format(self, record):
                s = super().format(record)
                return s + "\n"

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # 防止重复添加 handler
        if not logger.handlers:
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setFormatter(DoubleNewlineFormatter("%(asctime)s [%(levelname)s] %(message)s"))

            ch = logging.StreamHandler()
            ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

            logger.addHandler(fh)
            logger.addHandler(ch)

        return logger
    
    @staticmethod
    def register_signal_handlers(logger):
        def handle_exit(signum, frame):
            logger.warning("程序收到终止信号: %s", signum)
            logger.info("程序退出")
            sys.exit(0)

        # Ctrl+C
        signal.signal(signal.SIGINT, handle_exit)
        # kill 命令
        signal.signal(signal.SIGTERM, handle_exit)
        # 可选：终端关闭/挂起
        signal.signal(signal.SIGHUP, handle_exit)
        # 可选：程序退出请求
        signal.signal(signal.SIGQUIT, handle_exit)

