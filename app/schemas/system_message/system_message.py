from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class SystemMessageSchema(BaseModel):
    """系统消息模型"""
    id: Optional[int] = Field(None, description="主键ID")
    system_message: Optional[str] = Field(None, description="系统消息")
    is_actived: Optional[int] = Field(1, description="是否激活 1=激活 0=失效")

    model_config = ConfigDict(from_attributes=True)