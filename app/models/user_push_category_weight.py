from app.config.mysql_config import Base
from sqlalchemy import Column, Integer, DateTime, DECIMAL, ForeignKey, Index,String
from datetime import datetime
from sqlalchemy.orm import relationship

class UserPushCategoryWeightModel(Base):
    """
    用户推送分类权重表
    """
    __tablename__ = "user_push_category_weight"

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    push_config_id = Column(Integer, ForeignKey('user_push_config.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, comment='推送表ID')
    category_id = Column(Integer, nullable=False, comment='分类ID')
    category_name = Column(String(50), nullable=False, comment='分类名称')
    weight = Column(DECIMAL(5, 2), nullable=False, default=0.00, comment='分类权重')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, comment='修改时间')

    config = relationship(
        "UserPushConfigModel",
        back_populates="weights"
    )

    __table_args__ = (
        # 唯一索引: 同一个配置下，分类ID唯一
        Index('uk_config_category', 'push_config_id', 'category_id', unique=True),
    )