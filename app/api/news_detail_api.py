from fastapi import APIRouter, Query
from app.utils.result_response import Result
from app.services.news_detail_service import NewsDetailOperator
from app.services.news_service import NewsOperator
from app.schemas.news.new_schema import NewsSchema
from app.schemas.news_detail.news_detail_schema import NewsDetailsSchema
from app.schemas.news.news_response_schema import NewsResponse
from app.utils.logger import Logger
from app.services.rss_service import RssSourceOperator

router = APIRouter()
logger = Logger.setup_logger(Logger.set_file_date())

@router.get("/get_news_detail", response_model=Result[NewsResponse])
def get_news_detail(
    page:int = Query(1, gt=0, description="页码，从1开始"),
    page_size:int = Query(10, gt=0, le=100, description="每页数量，最大100")
):
    detail_service = NewsDetailOperator()
    news_detail_list = detail_service.get_pages_news(page, page_size)
    logger.info("请求数据：",news_detail_list)

    rss_service = RssSourceOperator()
    resp = []

    if news_detail_list["status"] == 200:
        for item in news_detail_list["news_detail_list"]:
            news_detail_item = NewsDetailsSchema.parse_obj(item)

            news_service = NewsOperator()
            news_data = news_service.get_news_by_id(news_detail_item.news_id)
            news = NewsSchema.parse_obj(news_data)

            rss_data = rss_service.get_rss_detail_by_url(news.source)

            result = NewsResponse()
            result.id = news_detail_item.id
            result.news_id = news_detail_item.news_id
            result.url = news.url
            result.title = news.title
            result.industry_category = news_detail_item.category_name
            result.one_sentence_summary = news_detail_item.ai_json_output["abstract"] or None
            result.ai_summary = news_detail_item.ai_json_output["summary"] or None
            result.keywords = news_detail_item.ai_json_output["keywords"] or None
            result.policy_risk = news_detail_item.ai_json_output["policy_risk"]["market_risk"] or None
            result.policy_compliance = news_detail_item.ai_json_output["policy_risk"]["policy_compliance"] or None
            result.rss_id = rss_data.id
            result.rss_tag = rss_data.name
            result.published_at = news.published_at
            result.data_source = news.source
            result.is_policy = news.is_policy
            resp.append(result)

    total = 0
    if "total" in news_detail_list:
        total = news_detail_list["total"]
    else:
        # 处理缺失的情况
        total = 0
    return Result.success(
        data={
            "list": resp,
            "page": page,
            "page_size": page_size,
            "total": total
        }
    )


            