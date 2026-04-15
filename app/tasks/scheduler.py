from fastapi import APIRouter
from app.utils.logger import Logger


scheduler_task = APIRouter()
logger = Logger.setup_logger(Logger.set_file_date())

@scheduler_task.on_event("startup")
def startup():
    """启动时执行"""
    from app.core.scheduler import scheduler
    from app.tasks.crwal_task import spider_rss
    if not scheduler.running:
        scheduler.start()
    spider_rss()
    logger.info("定时任务启动成功！")