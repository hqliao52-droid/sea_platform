from sqlalchemy import (
    Column, 
    Integer, 
    DateTime, 
    DECIMAL, 
    ForeignKey, 
    String, 
    func, 
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.config.pg_config import Base

class UserPushCategoryWeightModel(Base):
    """
    用户推送分类权重表
    """

    __tablename__ = "user_push_category_weight"
    __table_args__ = (
        # 唯一索引: 同一个配置下，分类ID唯一
        UniqueConstraint("push_config_id", "category_id", name="uk_config_category"),
        {"comment": "用户推送分类权重表"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    push_config_id = Column(
        Integer,
        ForeignKey("user_push_config.id", ondelete="CASCADE", onupdate="RESTRICT"),
        nullable=False,
        comment="推送表ID",
    )
    category_id = Column(Integer, nullable=False, comment="分类ID")
    category_name = Column(String(50), nullable=False, comment="分类名称")
    weight = Column(DECIMAL(5, 2), nullable=False, default=0.00, comment="分类权重")
    created_at = Column(DateTime, default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, comment="修改时间")

    config = relationship("UserPushConfigModel", back_populates="weights")


