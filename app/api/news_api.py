from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.result_response import Result
from app.database.mysql import get_db
from app.models.news_model import News
from app.schemas.new_schema import NewsSchema

router = APIRouter()


@router.get("/news")
async def get_news(db: Session = Depends(get_db)):
    news_list = db.query(News).limit(10).all()
    news_data = [NewsSchema.model_validate(news) for news in news_list]
    return Result.success(data=news_data)
