# app/schemas/rss_schema.py
from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    id: int = Field(description="用户ID")
    username: Optional[str] = Field(description="用户名")
    password: Optional[str] = Field(description="密码")
    
    nickname: Optional[str] = Field(None,description="昵称")
    phone: Optional[str] = Field(None,description="手机号")
    email: Optional[str] = Field(None,description="邮箱")
    city: Optional[str] = Field(None,description="所在城市")
    avatar: Optional[str] = Field(None,description="头像")
    status: Optional[int] = Field(None,description="状态")
    role: Optional[int] = Field(None,description="角色")
    created_time: Optional[datetime] = Field(None,description="创建时间")
    updated_time: Optional[datetime] = Field(None,description="更新时间")
    last_login_time: Optional[datetime] = Field(None,description="最后登录时间")
    last_login_ip: Optional[str] = Field(None,description="最后登录IP")
    

    model_config = ConfigDict(from_attributes=True)