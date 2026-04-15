from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.config.mysql_config import Base

class category(Base):
    """
    标签表模型
    """
    __tablename__ = "category"

    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True, 
        nullable=False,
        comment="主键ID"
    )
    
    tag_name = Column(
        String(255), 
        nullable=True,
        comment="类名"
    )

    example = Column(
        String(255), 
        comment="标签示例"
    )
    
    is_active = Column(
        Boolean, 
        nullable=True, 
        default=1,
        comment="启用状态 1: 是 0: 否"
    )
    
    updated_at = Column(
        DateTime, 
        nullable=True, 
        default=datetime.now,
        comment="更新时间"
    )
    
    created_at = Column(
        DateTime, 
        nullable=False, 
        default=datetime.now,
        comment="创建时间"
    )