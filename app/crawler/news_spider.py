from app.utils.logger import Logger
import feedparser,json
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
            "origin_msg": json.dumps(convert_entry_to_json(entry)),
            "source": url,
            "is_policy": 0,
            "ai_json_output": ""
        }
        news_list.append(news)
        mq_client.publish(news)
    return news_list


# 将 entry 转换为可序列化的字典
def convert_entry_to_json(entry):
    """将 feedparser entry 转换为 JSON 兼容的字典"""
    # feedparser 的对象继承自 dict，可以直接 dict()
    entry_dict = dict(entry)
    
    # 处理嵌套的不可序列化对象
    for key, value in entry_dict.items():
        if hasattr(value, '__dict__') or isinstance(value, (list, dict)):
            # 递归处理复杂对象
            try:
                json.dumps(value)
            except TypeError:
                entry_dict[key] = str(value)
    logger.info("转json后的entry:%s",json.dumps(entry))
    
    return entry_dict