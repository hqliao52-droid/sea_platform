from pydantic import Field, ConfigDict,BaseModel
from datetime import datetime
from typing import Optional

class UserPushNotifyChannelSchema(BaseModel):
    channel_address: str = Field(..., description="通知地址")
    channel_type: str = Field(..., description="通知方式")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    id: int = Field(None, description="id")
    is_enabled: int = Field(..., description="是否启用")
    priority: int = Field()
    # push_config_id: int = Field(..., description="推送配置表ID")

    model_config = ConfigDict(from_attributes=True)

class UserPushNotifyChannelResponseSchema(BaseModel):
    channel_address: str = Field(..., description="通知地址")
    channel_type: str = Field(..., description="通知方式")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    id: int = Field(None, description="id")
    is_enabled: int = Field(..., description="是否启用")
    priority: int = Field()
    push_config_id: int = Field(..., description="推送配置表ID")
    
    model_config = ConfigDict(from_attributes=True)
