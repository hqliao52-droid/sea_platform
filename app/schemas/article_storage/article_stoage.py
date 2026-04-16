from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ArticleStorageSchema(BaseModel):
    """文章存储模型"""
    id: Optional[int] = Field(None, description="主键ID")
    news_id: Optional[int] = Field(None, description="新闻ID")
    original_input: Optional[dict] = Field(None, description="原始URL")
    article_name: Optional[str] = Field(None, description="文章名称")
    created_at: Optional[datetime] = Field(None, description="创建时间")

    model_config = ConfigDict(from_attributes=True)
