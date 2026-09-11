from app.config.pg_config import Base
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Index,
    SmallInteger,
    String,
    UniqueConstraint,
    func
)
from sqlalchemy.orm import relationship

class UserPushNotifyChannelModel(Base):
    """
    用户推送通知渠道表
    """

    __tablename__ = "user_push_notify_channel"
    __table_args__ = (
        UniqueConstraint("push_config_id", "channel_type", name="uk_channel_type"),
        Index("push_config_id", "push_config_id"),
        {"comment": "用户推送通知渠道表"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="id")
    push_config_id = Column(
        Integer,
        ForeignKey("user_push_config.id", ondelete="CASCADE", onupdate="RESTRICT"),
        nullable=False,
        comment="推送配置表ID",
    )
    channel_type = Column(String(50), nullable=False, comment="通知方式")
    channel_address = Column(String(255), nullable=False, comment="通知地址")
    is_enabled = Column(SmallInteger, nullable=False, default=1, comment="是否启用")
    priority = Column(
        Integer,
        nullable=False,
        default=1,
        comment="优先级 1~5  1：最高优先级  5：最低优先级",
    )
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), comment="修改时间")

    """
    回到父对象
    """
    config = relationship("UserPushConfigModel", back_populates="channels")
