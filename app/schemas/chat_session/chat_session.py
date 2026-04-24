from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ChatSessionSchema(BaseModel):
    """会话模型"""
    id: Optional[int] = Field(None, description="会话ID(主键)")
    user_id: Optional[int] = Field(None, description="用户ID")
    llm_id: Optional[int] = Field(None, description="机器人ID")
    is_new_session: Optional[int] = Field(1, description="是否为新窗口 1=是 0=不是")
    session_topic: Optional[str] = Field(None, description="会话主题")
    is_deleted: Optional[int] = Field(0, description="软删除 1=是 0=否")
    created_time: Optional[datetime] = Field(None, description="创建时间")
    update_time: Optional[datetime] = Field(None, description="更新时间")

    model_config = ConfigDict(from_attributes=True)