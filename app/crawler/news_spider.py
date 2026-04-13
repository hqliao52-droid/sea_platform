from app.utils.logger import Logger
import feedparser
from app.utils.time_convert import parse_rss_date
from app.config.rabbitMq_config import MQClient

logger = Logger.setup_logger(Logger.set_file_date())
mq_client = MQClient()

def crawl_all_rss_sources(url):
    feed = feedparser.parse(url)
    entries = feed.entries
    news_list = []

    for entry in entries:
        title = entry.get("title", "")
        content = entry.get("summary", "")

        news = {
            "title": title,
            "url": entry.get("link", ""),
            "published_at": parse_rss_date(entry.get("published")),
            "content": content,
            "origin_msg": str(entry),
            "source": url,
            "authors": "",
            "keywords": "",
            "category": "",
            "ai_summary": "",
            "is_policy": 0,
        }
        news_list.append(news)
    mq_client.publish(news_list)
    return news_list