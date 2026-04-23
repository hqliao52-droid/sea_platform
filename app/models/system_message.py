from sqlalchemy import Column, Integer, String, SmallInteger
from app.config.mysql_config import Base

class SystemMessage(Base):
    __tablename__ = "system_message"
    __table_args__ = {'comment': '系统消息表'}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="主键ID"
    )
    system_message = Column(
        String(255),
        nullable=True,
        comment="系统消息"
    )
    is_actived = Column(
        SmallInteger,
        nullable=True,
        default=1,
        comment="是否激活 1=激活 0=失效"
    )