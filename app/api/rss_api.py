from app.services.rss_service import RssSourceOperator
from app.utils.result_response import Result
from fastapi import APIRouter

router = APIRouter()

rss = RssSourceOperator()
@router.get("/active_rss")
def get_rss_source_list():
    """获取所有激活 rss 源"""
    result = rss.get_active_rss_sources()
    return Result.success(data=result)
