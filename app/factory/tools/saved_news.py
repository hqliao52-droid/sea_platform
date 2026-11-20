
import json

from langchain.tools import tool
from pydantic import BaseModel, Field

from app.services.news_detail_service import NewsDetailOperator
from app.models.news_details_model import NewsDetail
from app.utils.log import logger

news_detail = NewsDetailOperator()

class SearchNewsInput(BaseModel):
    news_ids: list[int] = Field(description="新闻ID列表")

async def search_news(news_ids: list[int]) -> list[NewsDetail]:
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
    return []

@tool("check_news_length_or_summary")
async def check_news_length_or_summary(news_ids: list[int]) -> list:
    """
    根据用户提供的新闻id，返回新闻/文章/帖子的内容长度以及摘要
    判断后续是否需要阅读全文还是截取片段
    """
    news_list = await search_news(news_ids)
    news_summary = []
    logger.info(f">[tool调用] agent调用了{len(news_ids)}篇文章摘要")

    for index, news in enumerate(news_list):
        news_summary.append({
            "news_id": news.id,
            "position": f"用户引用的第{index+1}篇文章/新闻/帖子",
            "title": news.title,
            "summary": news.ai_origin_output.get("abstract", ""),
            "content_length": len(news.content),
        })
    return news_summary

@tool("search_saved_news", args_schema=SearchNewsInput)
async def search_saved_news(news_ids: list[int]) -> list:
    """
    根据用户提供的新闻id列表，返回用户引用的这些新闻/文章/帖子的内容
    注意：此工具返回的内容可能存在超长字符，调用此工具前，可考虑优先调用`check_news_length_or_summary`来决定是否需要阅读全文还是截取片段
    """
    refer_data = await search_news(news_ids)
    news_details = []
    logger.info(f">[tool调用] agent调用了{len(news_ids)}篇文章内容")
    for index, news in enumerate(refer_data):
        news_details.append({
            "news_id": news.id,
            "position": f"用户引用的第{index+1}篇文章/新闻/帖子",
            "title": news.title,
            "content": news.content,
        })
    return news_details