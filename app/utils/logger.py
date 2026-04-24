import logging
import os
from datetime import date
import logging.handlers
import queue

# 全局队列（关键！所有 logger 共用）
log_queue = queue.Queue(-1)

# 全局 listener（只启动一次）
listener = None

class Logger:
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
    
    @staticmethod
    def setup_logger(name: str, log_dir: str=None):
        def logs_path():
            # 获取当前文件所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 向上两级到达 项目 目录
            pro_root = os.path.dirname(os.path.dirname(current_dir))
            # 拼接 logs 目录
            logs_dir = os.path.join(pro_root, 'logs')
            return logs_dir
        log_dir = log_dir or logs_path()

        global listener

        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{name}.log")

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # ⚠️ 避免重复添加 handler
        if logger.handlers:
            return logger

        # ========= 核心：QueueHandler =========
        queue_handler = logging.handlers.QueueHandler(log_queue)
        logger.addHandler(queue_handler)

        # ========= listener 只启动一次 =========
        if listener is None:

            # 文件 handler
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s"
            )
            file_handler.setFormatter(file_formatter)

            # 控制台 handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(file_formatter)

            listener = logging.handlers.QueueListener(
                log_queue,
                file_handler,
                console_handler,
                respect_handler_level=True
            )
            listener.start()

        return logger

    @staticmethod
    def shutdown():
        global listener
        if listener:
            listener.stop()
