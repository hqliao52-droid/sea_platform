from app.config.mysql_config import Base
from sqlalchemy import Column, Integer, String, Double, DateTime
from datetime import datetime

class UserModel(Base):
    """
        用户表
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    username = Column(String(255), nullable=False, comment="用户名")

    password = Column(String(255), nullable=False, comment="密码")

    nickname = Column(String(255), nullable=False, comment="昵称")

    phone = Column(String(255), nullable=False, comment="手机号")

    email = Column(String(255), nullable=False, comment="邮箱")

    avatar = Column(String(255), nullable=False, comment="头像")

    status = Column(Integer, nullable=False, comment="状态")

    role = Column(Integer, nullable=False, comment="角色")

    city = Column(String(255), nullable=False, comment="所在城市")

    created_time = Column(DateTime, default=datetime.now, comment="创建时间")

    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    last_login_time = Column(DateTime, nullable=False, comment="最后登录时间")

    last_login_ip = Column(String(255), nullable=False, comment="最后登录IP")
