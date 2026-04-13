from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.config.mysql_config import Base

class News(Base):
    """
    新闻资讯表
    """

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # 新闻标题
    title = Column(String(255), nullable=False)

    # url原始链接
    url = Column(String(255))

    # RSS来源
    source = Column(String(255))

    # 原文内容
    content = Column(Text)

    # 文章作者
    authors = Column(String(255))

    # 关键词
    keywords = Column(String(255))

    # 行业分类
    category = Column(String(255))

    # AI摘要
    ai_summary = Column(Text)

    # 文章摘要
    origin_msg = Column(Text)

    # 发布时间
    published_at = Column(DateTime)

    # 创建时间
    created_at = Column(DateTime, default=datetime.now)

    is_policy = Column(Integer, default=0)