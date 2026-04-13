from dateutil import parser
from datetime import datetime

def parse_rss_date(date_string):
    """
    通用日期解析，支持多种格式
    """
    if not date_string:
        return datetime.now()
    
    try:
        # dateutil 可以自动识别绝大多数日期格式
        dt = parser.parse(date_string)
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_date
    except Exception as e:
        print(f"日期解析失败: {date_string}, 错误: {e}")
        return datetime.now()
