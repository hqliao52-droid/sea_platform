from sqlalchemy import Column, Integer, String, DateTime, SmallInteger
from datetime import datetime
from app.config.mysql_config import Base

class ChatSession(Base):
    __tablename__ = "chat_session"
    __table_args__ = {'comment': '记录用户一次完整对话窗口'}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="会话ID(主键)"
    )
    user_id = Column(
        Integer,
        nullable=False,
        comment="用户ID",
        index=True
    )
    llm_id = Column(
        Integer,
        nullable=False,
        comment="机器人ID"
    )
    is_new_session = Column(
        SmallInteger,
        nullable=False,
        default=1,
        comment="是否为新窗口 1=是 0=不是"
    )
    is_deleted = Column(
        SmallInteger,
        nullable=True,
        default=0,
        comment="软删除 1=是 0=否"
    )
    created_time = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        comment="创建时间"
    )
    update_time = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )
    session_topic = Column(
        String(255),
        nullable=True,
        default=None,
        comment="会话主题"
    )