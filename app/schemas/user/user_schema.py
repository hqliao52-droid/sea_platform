# app/schemas/rss_schema.py
from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    id: int = Field(description="用户ID")
    user_name: Optional[str] = Field(None,description="用户名")
    user_ip: Optional[str] = Field(None,description="用户IP")
    mac_ip: Optional[str] = Field(None,description="MAC地址")
    city: Optional[str] = Field(None,description="所在城市")
    created_at: Optional[datetime] = Field(None,description="创建时间")

    model_config = ConfigDict(from_attributes=True)