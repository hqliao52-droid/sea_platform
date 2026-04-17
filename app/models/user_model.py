from app.config.mysql_config import Base
from sqlalchemy import Column, Integer, String, Double, DateTime
from datetime import datetime

class UserModel(Base):
    """
        用户表
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    user_name = Column(String(255), nullable=False, comment="用户名")

    user_ip = Column(String(255), nullable=False, comment="用户IP")

    mac_ip = Column(String(255), nullable=False, comment="MAC地址")

    city = Column(String(255), nullable=False, comment="所在城市")

    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
