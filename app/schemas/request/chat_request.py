from typing import Literal, Optional
from urllib.parse import urlparse
from app.models.user_model import UserModel

from pydantic import BaseModel, Field, field_validator, model_validator


class ChatRequest(BaseModel):
    app_id: str = Field(..., description="应用ID")
    session_id: str | None = Field(None, description="会话ID")
    query: str = Field(..., description="用户问题")
    files: list[str] | None = Field(None, description="上传的文件")