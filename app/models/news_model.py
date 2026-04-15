from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.config.mysql_config import Base

class News(Base):
    """
    新闻资讯表
    """

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    category_id = Column(Integer,nullable=False,description="分类ID")

    category_name = Column(String(255),nullable=False,description="分类名称")

    # 新闻标题
    title = Column(String(255), nullable=False,description="新闻标题")

    # url原始链接
    url = Column(String(255), nullable=False,description="新闻URL")

    # RSS来源
    source = Column(String(255),description="RSS来源")

    # 发布时间
    published_at = Column(DateTime,description="发布时间")

    # 创建时间
    created_at = Column(DateTime, default=datetime.now,description="创建时间")

    # 是否是政策类
    is_policy = Column(Integer, default=0,description="是否是政策类")
