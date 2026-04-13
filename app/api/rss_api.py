from services.rss_service import RssSourceOperator
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.news_schema import NewsOut
from app.utils.result_response import Result

router = APIRouter()


@router.get("/", response_model=list[NewsOut])
def get_rss_source_list():
    """获取所有激活 rss 源"""
    list = RssSourceOperator.get_active_rss_sources()
    return Result.success(data=list)
