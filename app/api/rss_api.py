from app.services.rss_service import RssSourceOperator
from app.utils.result_response import Result
from fastapi import APIRouter,Query  

router = APIRouter()

rss = RssSourceOperator()
@router.get("/active_rss")
def get_rss_source_list():
    """获取所有激活 rss 源"""
    result = rss.get_active_rss_sources()
    return Result.success(data=result)

@router.get("/get_by_url", summary="根据url获取rss源")
async def get_by_url(url: str = Query(..., description="RSS源的URL地址")):
    """根据url获取rss源"""
    result = rss.get_rss_detail_by_url(url)
    return Result.success(data=result)