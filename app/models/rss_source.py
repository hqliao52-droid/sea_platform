from sqlalchemy import Column, Integer, String, Double, DateTime, func

from app.config.pg_config import Base


class RssSource(Base):
    """
    Rss 源
    """

    __tablename__ = "rss_source"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    # 源名称
    name = Column(String(255), nullable=False, comment="源名称")

    # 源链接
    url = Column(String(255), nullable=False, comment="源链接")

    # 分类
    category = Column(String(255), nullable=False, comment="分类")

    # 是否激活
    is_active = Column(Integer, default=1, comment="是否激活")

    # 是否需要 api key
    is_api_key = Column(Integer, default=0, comment="是否需要 api key")

    # 更新频率
    update_rate = Column(Integer, default=60 * 60 * 12, comment="更新频率")

    # 热度
    hot_rate = Column(Double, comment="热度")

    # 源评分
    source_score = Column(Double, comment="源评分")

    # 创建时间
    created_at = Column(DateTime, default=func.now, comment="创建时间")
