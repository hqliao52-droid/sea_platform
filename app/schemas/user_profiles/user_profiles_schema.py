from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(None, description="用户ID")
    user_id: Optional[int] = Field(None, description="用户ID")
    _metadata: Optional[dict] = Field(None, description="用户元数据（画像）")
    created_time: Optional[datetime] = Field(None, description="创建时间")
