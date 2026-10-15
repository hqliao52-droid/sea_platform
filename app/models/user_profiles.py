from sqlalchemy import (
    Column, Integer, DateTime, Index, text
)
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.config.pg_config import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"
    __table_args__ = (
        Index("user_profiles", "user_id", postgresql_using="btree"),
        {"comment": "用户的画像表"},
    )

    id = Column(
        Integer, primary_key=True, autoincrement=True, comment="主键ID"
    )
    user_id = Column(Integer, nullable=False, comment="用户ID")

    # _metadata，但映射到数据库列 "metadata"
    metadata_ = Column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text(
            """'{"data": [{"datetime": "-", "profile": "-"}]}'::jsonb"""
        ),
        comment="用户元数据（画像）",
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="创建时间",
    )