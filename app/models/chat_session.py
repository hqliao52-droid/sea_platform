from sqlalchemy import Column, Integer, String, DateTime, SmallInteger
from datetime import datetime
from app.config.mysql_config import Base

class ChatSession(Base):
    __tablename__ = "chat_session"
    __table_args__ = {'comment': '记录用户一次完整对话窗口'}

    id = Column(
        String(64),
        primary_key=True,
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
    status = Column(
        SmallInteger,
        nullable=False,
        default=1,
        comment="状态：1进行中 2已关闭"
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