from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class LlmApiLogSchema(BaseModel):
    """LLM接口调用日志模型"""
    id: Optional[int] = Field(None, description="主键ID")
    message_id: Optional[int] = Field(None, description="关联消息ID")
    session_id: Optional[str] = Field(None, description="会话窗口ID")
    model_name: Optional[str] = Field(None, description="模型名")
    temperature: Optional[float] = Field(None, description="温度")
    prompt_tokens: Optional[int] = Field(0, description="提示词token消耗")
    completion_tokens: Optional[int] = Field(0, description="生成消息所消耗的token")
    total_tokens: Optional[int] = Field(0, description="总token")
    status: Optional[int] = Field(0, description="消息状态 0=待处理, 1=已完成, 2=处理中, 3=失败（如超时/报错）")
    error_msg: Optional[str] = Field(None, description="失败消息")
    ip_address: Optional[str] = Field(None, description="用户地址")
    user_client: Optional[str] = Field(None, description="用户的客户端信息")
    sensitive_check_result: Optional[int] = Field(0, description="敏感词检测结果")
    created_time: Optional[datetime] = Field(None, description="创建时间")

    model_config = ConfigDict(from_attributes=True)