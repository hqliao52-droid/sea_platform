# app/schemas/new_schema.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class NewsSchema(BaseModel):
    id: int
    title: str
    url: Optional[str] = None
    source: Optional[str] = None
    content: Optional[str] = None
    authors: Optional[str] = None
    keywords: Optional[str] = None
    category: Optional[str] = None
    ai_summary: Optional[str] = None
    origin_msg: Optional[str] = None
    published_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    is_policy: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
