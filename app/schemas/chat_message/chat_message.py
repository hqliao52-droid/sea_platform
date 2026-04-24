from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ChatMessageSchema(BaseModel):
    """聊天消息模型"""
    id: Optional[int] = Field(None, description="消息ID")
    session_id: Optional[str] = Field(None, description="会话ID")
    user_id: Optional[int] = Field(None, description="用户ID")
    message_type: Optional[int] = Field(None, description="1用户 2机器人 3系统 4工具")
    content: Optional[str] = Field(None, description="消息内容")
    llm_refer_data: Optional[str] = Field(None, description="引用资料")
    llm_refer_data_id: Optional[int] = Field(None, description="引用资料ID")
    user_rating: Optional[int] = Field(0, description="用户评分 取值：1-5分或1=点赞, 0=无反馈, -1=点踩")
    curren_user_ip_info: Optional[str] = Field(None, description="用户IP信息")
    user_feedback: Optional[str] = Field(None, description="用户使用反馈内容（用于后续优化模型或prompt）")
    is_deleted: Optional[int] = Field(0, description="是否删除？ 1=是  0=否")
    created_time: Optional[datetime] = Field(None, description="创建时间")

    model_config = ConfigDict(from_attributes=True)