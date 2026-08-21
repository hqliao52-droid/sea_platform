from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class ChatMessageSchema(BaseModel):
    """聊天消息模型"""

    id: Optional[int] = Field(None, description="消息ID")
    session_id: Optional[int] = Field(None, description="会话ID")
    user_id: Optional[int] = Field(None, description="用户ID")
    task_id: Optional[str] = Field(None, description="任务ID")
    pre_id: Optional[int] = Field(
        None,
        description="引用消息ID 如果是LLM的回答，就不能置空，并且对应值是回复的消息的ID",
    )
    role: Optional[str] = Field(None, description="角色")
    message_type: Optional[int] = Field(None, description="1用户 2机器人 3系统 4工具")
    content: Optional[str] = Field(None, description="消息内容")
    llm_refer_data: Optional[List[str]] = Field(None, description="引用资料")
    llm_refer_data_id: Optional[list] = Field(None, description="引用资料ID")
    status: Optional[str] = Field(0, description="消息状态 done/streaming/exception")
    user_rating: Optional[int] = Field(
        0, description="用户评分 取值：1-5分或1=点赞, 0=无反馈, -1=点踩"
    )
    curren_user_ip_info: Optional[str] = Field(None, description="用户IP信息")
    user_feedback: Optional[str] = Field(
        None, description="用户使用反馈内容（用于后续优化模型或prompt）"
    )
    is_deleted: Optional[int] = Field(0, description="是否删除？ 1=是  0=否")
    created_time: Optional[datetime] = Field(None, description="创建时间")

    model_config = ConfigDict(from_attributes=True)


class ChatMsg(BaseModel):
    query: str
    user_id: int
    session_id: int
    news_ids: Optional[List[int]] = None
