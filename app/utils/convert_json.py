import json,time

def safe_json(data):
    """ JSON 转换"""
    return json.dumps(data, default=str, ensure_ascii=False)

def clean_feed_data(entry: dict):
    """清洗 feedparser 数据（用于入库 / JSON化）"""

    if "published_parsed" in entry and entry["published_parsed"]:
        entry["published_parsed"] = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            entry["published_parsed"]
        )

    return entry

def rss_date_convert(date):
    return time.strftime(
            "%Y-%m-%d %H:%M:%S",
            date
        )