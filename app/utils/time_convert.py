from dateutil import parser
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

# 数据库里的 timestamp 字段是不带时区的，项目内统一按 Asia/Shanghai 落库
LOCAL_TZ = ZoneInfo("Asia/Shanghai")


def _to_naive_local(dt: datetime) -> datetime:
    """带时区的时间先转成 Asia/Shanghai，再去掉 tzinfo（timestamp without time zone）"""
    if dt.tzinfo is None:
        return dt
    return dt.astimezone(LOCAL_TZ).replace(tzinfo=None)


def to_datetime(value):
    """
    把 str / datetime / date / 空值 统一转成 datetime（无时区）

    - None、空字符串、无法解析的值 -> None
    - datetime -> 去掉时区后返回
    - date -> 当天 00:00:00
    - str -> 交给 dateutil 自动识别（支持 "2026-11-19T12:13:51.708549"、
             "2026-11-19 12:13:51"、RFC 822 等格式）

    注意：数据库 timestamp 字段必须传 datetime。直接传字符串时 SQLAlchemy 会按
    字符串类型绑定参数（= $2::VARCHAR），PostgreSQL 会报
    "operator does not exist: timestamp without time zone = character varying"
    """
    if value is None or value == "":
        return None

    if isinstance(value, datetime):
        return _to_naive_local(value)

    if isinstance(value, date):
        return datetime.combine(value, time.min)

    try:
        # dateutil 可以自动识别绝大多数日期格式
        return _to_naive_local(parser.parse(str(value)))
    except (ValueError, OverflowError, TypeError) as e:
        print(f"日期解析失败: {value}, 错误: {e}")
        return None


def parse_rss_date(date_string):
    """
    通用日期解析，支持多种格式

    统一返回 "YYYY-MM-DD HH:MM:SS" 字符串；解析失败返回 None。
    不要用 datetime.now() 兜底：同一篇新闻每次抓取都会得到不同的发布时间，
    既污染排序，也会让去重永远失效。
    """
    dt = to_datetime(date_string)
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S")
