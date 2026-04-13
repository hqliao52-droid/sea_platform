from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.result_response import Result
from app.config.mysql_config import get_db
from app.models.news_model import News
from app.schemas.new_schema import NewsSchema
from app.utils.logger import Logger


router = APIRouter()
logger = Logger.setup_logger(Logger.set_file_date())

@router.get("/news")
async def get_news(db: Session = Depends(get_db)):
    news_list = db.query(News).limit(10).all()
    news_data = [NewsSchema.model_validate(news) for news in news_list]
    return Result.success(data=news_data)

@router.on_event("startup")
async def startup():
    """启动时执行"""
    from app.core.scheduler import scheduler
    from app.tasks.crwal_task import spider_rss
    if not scheduler.running:
        scheduler.start()
    await spider_rss()
    logger.info("定时任务启动成功！")
    

