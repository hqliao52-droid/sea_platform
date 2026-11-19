
from langchain.tools import tool
from pydantic import BaseModel, Field

from app.services.news_detail_service import NewsDetailOperator
from app.models.news_details_model import NewsDetail
from app.utils.log import logger

news_detail = NewsDetailOperator()

class SearchNewsInput(BaseModel):
    news_ids: list[int] = Field(description="新闻ID列表")

async def search_news(news_ids: list[int]) -> list[NewsDetail] | None:
    """
    根据用户提供的新闻id列表，返回用户引用的这些新闻/文章/帖子的内容
    """
    refer_data: list[NewsDetail] = []
    if news_ids:
        for id in news_ids:
            news = await news_detail.get_news_detail_by_id(id)
            logger.info(f"用户当前引用的文章{news.title}")
            refer_data.append(news)
        return refer_data
    return None

@tool("check_news_content_length")
async def check_news_content_length(news_ids: list[int]) -> tuple[int, str]:
    """
    根据用户提供的新闻id，返回新闻/文章/帖子的内容长度以及摘要
    判断后续是否需要截断
    """
    news = await search_news(news_ids)

@tool("search_saved_news", args_schema=SearchNewsInput)
async def search_saved_news(news_ids: list[int]) -> str:
    """
    根据用户提供的新闻id列表，返回用户引用的这些新闻/文章/帖子的内容
    注意：此工具返回的内容可能存在超长字符，调用此工具前，可考虑优先调用``
    """