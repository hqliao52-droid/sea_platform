from app.utils.logger import Logger
import feedparser
from app.tasks.ai_task import llm_check_outreach_news
from app.crud.data_crud.news import news_crud

logger = Logger.setup_logger(Logger.set_file_date())


async def run_single_rss_task(name, url):
    logger.info(f"开始爬取：{name}")

    try:
        news_list = await crawl_all_rss_sources(url)

        # 数据库 insert 必须 await！
        for news in news_list:
            await news_crud.insert(news)  # 这里加 await！

        logger.info(f"{name} 爬取完成：{len(news_list)} 条")

    except Exception as e:
        logger.error(f"{name} 爬取失败：{str(e)}")

async def crawl_all_rss_sources(url):
    feed = feedparser.parse(url)
    entries = feed.entries
    news_list = []

    for entry in entries:
        title = entry.get("title", "")
        content = entry.get("summary", "")
        result = llm_check_outreach_news(title, content)

        news = {
            "title": title,
            "url": entry.get("link", ""),
            "published_at": entry.get("published"),
            "content": content,
            "origin_msg": str(entry),
            "source": url,
            "authors": "",
            "keywords": "",
            "category": "",
            "ai_summary": "",
            "is_policy": 1 if result == "1" else 0
        }
        news_list.append(news)

    return news_list