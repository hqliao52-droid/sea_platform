from app.config.mysql_config import Base
from sqlalchemy import Column, Integer, String, Double, DateTime
from datetime import datetime

class RssSource(Base):
    """
        Rss 源
    """
    __tablename__ = "rss_source"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True,)

    # 源名称
    name = Column(String(255))

    # 源链接
    url = Column(String(255))

    # 分类
    category = Column(String(255))

    # 是否激活 
    is_active = Column(Integer, default=1)

    # 是否需要 api key
    is_api_key = Column(Integer, default=0)

    # 更新频率
    update_rate = Column(Integer, default=60*60*12)

    # 热度
    hot_rate = Column(Double)

    # 源评分
    source_score = Column(Double)

    # 创建时间
    created_at = Column(DateTime, default=datetime.now)

