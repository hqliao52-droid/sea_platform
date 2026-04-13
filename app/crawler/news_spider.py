from app.utils.logger import Logger
import feedparser
from app.tasks.ai_task import llm_check_outreach_news
from app.crud.data_crud.news import news_crud

logger = Logger.setup_logger(Logger.set_file_date())


async def run_single_rss_task(name, url):
    """执行单个RSS爬取 → 写MySQL → 写Qdrant"""
    logger.info(f"开始爬取：{name}")

    try:
        # 1. 爬取解析
        news_list = await crawl_all_rss_sources(url)

        # 2. 写入MySQL
        for news in news_list:
            news_crud.insert(news)

        logger.info(f"✅ {name} 爬取完成：{len(news_list)} 条")

    except Exception as e:
        logger.error(f"❌ {name} 爬取失败：{str(e)}")

def crawl_all_rss_sources(url):
    """爬取RSS源"""
    feed = feedparser.parse(url)
    entries = feed.entries
    news_list = []

    for entry in entries:
        title = entry.get("title", "")
        content = entry.get("summary", "")
        result = llm_check_outreach_news(title,content)
        news = {
            "title": entry.get("title", ""),
            "url": entry.get("link", ""),
            "published_at": entry.get("published"),
            "content": entry.get("summary", ""),
            "origin_msg": str(entry),
            "source": url,
            "authors": "",
            "keywords": "",
            "category": "",
            "ai_summary": ""
        }
        if result == "1":
            news.update({"is_policy":1})
        else:
            news.update({"is_policy":0})
        
        news_list.append(news)
    
    return news_list