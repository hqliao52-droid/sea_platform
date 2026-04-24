from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger, SmallInteger
from datetime import datetime
from app.config.mysql_config import Base

class ChatMessage(Base):
    __tablename__ = "chat_message"
    __table_args__ = {'comment': '存储用户 / LLM 的每一条消息内容'}

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="消息ID"
    )
    session_id = Column(
        String(64),
        nullable=False,
        comment="会话ID",
        index=True
    )
    user_id = Column(
        Integer,
        nullable=False,
        comment="用户ID"
    )
    message_type = Column(
        SmallInteger,
        nullable=False,
        comment="1用户 2机器人 3系统 4工具"
    )
    content = Column(
        Text(None),
        nullable=False,
        comment="消息内容"
    )
    llm_refer_data = Column(
        Text,
        nullable=True,
        comment="引用资料"
    )
    llm_refer_data_id = Column(
        Integer,
        nullable=True,
        default=None,
        comment="引用资料ID"
    )
    user_rating = Column(
        SmallInteger,
        nullable=True,
        default=0,
        comment="用户评分 取值：1-5分或1=点赞, 0=无反馈, -1=点踩"
    )
    current_user_ip_info = Column(
        String(255),
        nullable=True,
        default=None,
        comment="用户IP信息"
    )
    user_feedback = Column(
        String(500),
        nullable=True,
        default=None,
        comment="用户使用反馈内容（用于后续优化模型或prompt）"
    )
    is_deleted = Column(
        SmallInteger,
        nullable=True,
        default=0,
        comment="是否删除？ 1=是  0=否"
    )
    created_time = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
        comment="创建时间"
    )