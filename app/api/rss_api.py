from app.services.rss_service import RssSourceOperator
from app.utils.result_response import Result
from app.schemas.rss_shema import RssSchema

router = APIRouter()


@router.get("/active_rss", response_model=list[RssSchema])
def get_rss_source_list():
    """获取所有激活 rss 源"""
    list = RssSourceOperator.get_active_rss_sources()
    result = [RssSchema.from_orm(item) for item in list]
    return Result.success(data=result)
