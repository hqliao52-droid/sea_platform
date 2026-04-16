from app.utils.logger import Logger
import feedparser
from app.utils.time_convert import parse_rss_date
from app.config.rabbitMq_config import MQClient
from app.utils.html_cleaner import clean_html_for_all_platform

logger = Logger.setup_logger(Logger.set_file_date())
mq_client = MQClient()

def crawl_all_rss_sources(url):
    feed = feedparser.parse(url)
    entries = feed.entries
    news_list = []

    for entry in entries:
        title = entry.get("title", "")
        content = entry.get("summary", "")

        safe_content = clean_html_for_all_platform(content)

        news = {
            "title": title,
            "url": entry.get("link", ""),
            "published_at": parse_rss_date(entry.get("published")),
            "content": safe_content,
            "origin_msg": entry, 
            "source": url,
            "is_policy": 0,
            "ai_json_output": ""
        }
        news_list.append(news)
        mq_client.publish(news)
    return news_list
