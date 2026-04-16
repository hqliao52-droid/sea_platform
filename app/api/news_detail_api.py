from fastapi import APIRouter, Query
from app.utils.result_response import Result
from app.services.news_detail_service import NewsDetailOperator
from app.services.news_service import NewsOperator
from app.schemas.news_detail.news_detail_response_schema import NewsDetailResponse
from app.schemas.news_detail.news_detail_page_resp import NewsDetailsPageSchema
from app.utils.logger import Logger
from app.services.rss_service import RssSourceOperator

router = APIRouter()
logger = Logger.setup_logger(Logger.set_file_date())

@router.get("/get_news_detail", response_model=Result[NewsDetailsPageSchema])
def get_news_detail(
    page:int = Query(1, gt=0, description="页码，从1开始"),
    page_size:int = Query(10, gt=0, le=100, description="每页数量，最大100")
):
    detail_service = NewsDetailOperator()
    news_detail_list = detail_service.get_pages_news(page, page_size)

    rss_service = RssSourceOperator()
    resp = []

    if news_detail_list["status"] == 200:
        news_service = NewsOperator()
        for item in news_detail_list["news_detail_list"]:
            news_data = news_service.get_news_by_id(item.news_id)
            rss_data = rss_service.get_rss_detail_by_url(news_data.source)

            result = NewsDetailResponse()
            result.id = item.id
            result.news_id = item.news_id
            result.url = news_data.url
            result.title = news_data.title
            result.industry_category = item.category_name
            result.one_sentence_summary = item.ai_origin_output["summary"] or None
            result.ai_summary = item.ai_origin_output["abstract"] or None
            result.keywords = item.ai_origin_output["keywords"] or None
            result.policy_risk = item.ai_origin_output["policy_risk"]["market_risk"] or None
            result.policy_compliance = item.ai_origin_output["policy_risk"]["policy_compliance"] or None
            result.rss_id = rss_data.id
            result.rss_tag = rss_data.name
            result.published_at = news_data.published_at
            result.data_source = news_data.source
            result.is_policy = news_data.is_policy
            resp.append(result)

    total = 0
    if "total" in news_detail_list:
        total = news_detail_list["total"]
    else:
        # 处理缺失的情况
        total = 0
    
    r = NewsDetailsPageSchema()
    r.page = page
    r.page_size = page_size
    r.result = resp
    r.total = total
    logger.info(f"返回数据：{resp}")
    return Result.success(r)


            