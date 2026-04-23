from sqlalchemy import Column, Integer, String, DateTime, Float, BigInteger, SmallInteger
from datetime import datetime
from app.config.mysql_config import Base

class LlmApiLog(Base):
    __tablename__ = "llm_api_log"
    __table_args__ = {'comment': 'LLM接口调用日志'}

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="主键ID"
    )
    message_id = Column(
        BigInteger,
        nullable=False,
        comment="关联消息ID",
        index=True
    )
    session_id = Column(
        String(64),
        nullable=False,
        comment="会话窗口ID",
        index=True
    )
    model_name = Column(
        String(100),
        nullable=True,
        comment="模型名"
    )
    temperature = Column(
        Float,
        nullable=True,
        comment="温度"
    )
    prompt_tokens = Column(
        Integer,
        nullable=True,
        default=0,
        comment="提示词token消耗"
    )
    completion_tokens = Column(
        Integer,
        nullable=True,
        default=0,
        comment="生成消息所消耗的token"
    )
    total_tokens = Column(
        Integer,
        nullable=True,
        default=0,
        comment="总token"
    )
    status = Column(
        SmallInteger,
        nullable=True,
        default=0,
        comment="消息状态 0=待处理, 1=已完成, 2=处理中, 3=失败（如超时/报错）"
    )
    error_msg = Column(
        String(1000),
        nullable=True,
        comment="失败消息"
    )
    ip_address = Column(
        String(64),
        nullable=True,
        comment="用户地址"
    )
    user_client = Column(
        String(500),
        nullable=True,
        comment="用户的客户端信息"
    )
    sensitive_check_result = Column(
        SmallInteger,
        nullable=True,
        default=0,
        comment="敏感词检测结果"
    )
    created_time = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
        comment="创建时间"
    )