from sqlalchemy import Column, Integer, String, DateTime,JSON
from datetime import datetime
from app.config.mysql_config import Base

class ArticleStorage(Base):
    __tablename__ = "article_storage"
    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True, 
        nullable=False,
        comment="主键ID"
    )
    news_id = Column(
        Integer, 
        nullable=False,
        comment="新闻ID"
    )
    article_name = Column(
        String(255), 
        nullable=False,
        comment="文章名称"
    )
    created_at = Column(
        DateTime, 
        default=datetime.now,
        comment="创建时间"
    )
    origin_input = Column(
        JSON, 
        nullable=False,
        comment="原始URL"
    )