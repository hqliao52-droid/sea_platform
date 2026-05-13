from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, SmallInteger, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.mysql_config import Base

class UserPushConfigModel(Base):
    """
    用户推送配置表
    """
    __tablename__ = "user_push_config"

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    user_id = Column(Integer, nullable=False, unique=True, comment='用户ID')
    max_push_amount = Column(Integer, nullable=False, comment='最大消息推送数量')
    is_enabled = Column(SmallInteger, nullable=False, default=0, comment='是否开启推送')
    
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 定义关系 (可选，方便后续查询关联数据)
    channels = relationship("UserPushNotifyChannelModel", back_populates="config")
    weights = relationship("UserPushCategoryWeightModel", back_populates="config")

    __table_args__ = (
        Index('idx_is_enabled', 'is_enabled'),
        Index('idx_created_at', 'created_at'),
    )