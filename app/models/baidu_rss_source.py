from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, Float
from datetime import datetime
from app.config.mysql_config import Base

class BaiduRssSource(Base):
    __tablename__ = "baidu_rss_source"
    __table_args__ = {
        'comment': 'RSS地址——feedparser',
        'mysql_engine': 'InnoDB',
        'mysql_row_format': 'DYNAMIC'
    }

    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True, 
        nullable=False,
        comment="主键ID"
    )
    name = Column(
        String(255),
        nullable=True,
        comment="目标网站名称"
    )
    url = Column(
        String(255),
        nullable=True,
        comment="目标网站URL"
    )
    category = Column(
        String(255),
        nullable=True,
        comment="目录"
    )
    is_child = Column(
        SmallInteger,
        nullable=True,
        default=1,
        comment="是否为子类rss"
    )
    parent_id = Column(
        SmallInteger,
        nullable=True,
        comment="父节点ID"
    )
    is_active = Column(
        SmallInteger,
        nullable=True,
        default=1,
        comment="是否可用 1:可用 0:不可用"
    )
    is_api_key = Column(
        SmallInteger,
        nullable=True,
        default=0,
        comment="是否需要API秘钥 1：是 0：否"
    )
    update_rate = Column(
        Integer,
        nullable=True,
        comment="更新频率"
    )
    hot_rate = Column(
        Float,
        nullable=True,
        comment="热点率"
    )
    source_score = Column(
        Float,
        nullable=True,
        comment="综合分数"
    )
    created_at = Column(
        DateTime,
        nullable=True,
        default=datetime.now,
        onupdate=datetime.now,
        comment="构建时间"
    )