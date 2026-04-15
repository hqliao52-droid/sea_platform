from fastapi import APIRouter, Query
from app.utils.result_response import Result
from app.services.news_service import NewsOperator
from app.schemas.news.new_schema import NewsSchema
from app.schemas.news.news_response_schema import NewsResponse
from app.utils.logger import Logger
from app.services.rss_service import RssSourceOperator

router = APIRouter()
logger = Logger.setup_logger(Logger.set_file_date())

@router.get("/get_news")
def get_news(
    # 分页参数：页码，默认第1页
    page: int = Query(1, gt=0, description="页码，从1开始"),
    # 分页参数：每页条数，默认10条
    page_size: int = Query(10, gt=0, le=100, description="每页数量，最大100"),
):
    service = NewsOperator()
    service_data = service.get_pages_news(page, page_size)
    logger.info("请求数据：",service_data)
    resp = []
    operator = RssSourceOperator()
    if service_data["status"] == 200:
        for item in service_data["news_list"]:
            data_schema = NewsSchema.parse_obj(item)
            rss_data = operator.get_rss_detail_by_url(data_schema.source)

            # 填充数据-基本信息
            result = NewsResponse()
            result.id = data_schema.id
            result.url = data_schema.url
            result.title = data_schema.title
            result.is_policy = data_schema.is_policy
            result.data_source = data_schema.source
            result.rss_tag = rss_data.name
            result.rss_id = rss_data.id
            result.published_at = data_schema.published_at
            if data_schema.is_policy == 1:
                # AI分析
                result.industry_category = data_schema.ai_json_output["industry_category"] or None
                result.one_sentence_summary = data_schema.ai_json_output["summary"] or None
                result.ai_summary = data_schema.ai_json_output["abstract"] or None
                result.keywords = data_schema.ai_json_output["keywords"] or None
                result.policy_risk = data_schema.ai_json_output["policy_risk"]["market_risk"] or None
                result.policy_compliance = data_schema.ai_json_output["policy_risk"]["policy_compliance"] or None
                
            resp.append(result)
            
    total = service_data["total"]
        

    
    # 返回带分页信息的成功结果
    return Result.success(
        data={
            "list": resp,
            "page": page,
            "page_size": page_size,
            "total": total
        }
    )

