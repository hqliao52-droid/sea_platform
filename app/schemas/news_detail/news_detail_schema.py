from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any

class NewsDetailsSchema(BaseModel):
    id: Optional[int] = Field(None, description="主键ID")
    news_id: Optional[int] = Field(None, description="父ID")
    category_id: Optional[int] = Field(None, description="栏目/类别-id")
    category_name: Optional[str] = Field(None, description="栏目/类别")
    title: Optional[str] = Field(None, description="文章标题")
    authors: Optional[str] = Field(None, description="文章作者")
    content: Optional[str] = Field(None, description="正文")
    url: Optional[str] = Field(None, description="文章原始url")
    watched: Optional[int] = Field(0, description="访问量")
    keywords: Optional[str] = Field(None, description="关键词")
    ai_origin_output: Optional[Dict[str, Any]] = Field(None, description="AI解析输出")
    summary: Optional[str] = Field(None, description="内容摘要")
    origin_entry: Optional[dict] = Field(None, description="原始entry")
    in_full_page: Optional[str] = Field(None, description="全文")
    publiced_at: Optional[datetime] = Field(None, description="发布时间")
    created_at: Optional[datetime] = Field(None, description="创建时间")

    model_config = ConfigDict(from_attributes=True)