from app.services.rss_service import RssSourceOperator
from app.utils.result_response import Result
from fastapi import APIRouter,Query  
# from app.services.baidu_rss_service import BaiduRssSourceOperator

router = APIRouter()

rss = RssSourceOperator()
# baidu_rss = BaiduRssSourceOperator()
@router.get("/active_rss")
def get_rss_source_list():
    """获取所有激活 rss 源"""
    result = rss.get_active_rss_sources()
    return Result.success(data=result)

@router.get("/get_by_id", summary="根据url获取rss源")
async def get_by_id(id: int = Query(..., description="RSS源的id")):
    """根据url获取rss源"""
    print(f"入参：{id}")
    result = rss.get_by_id(id)
    return Result.success(data=result)