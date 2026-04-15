# app/schemas/new_schema.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional,Union


class NewsSchema(BaseModel):
    id: int
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    title: str
    url: Optional[str] = None
    source: Optional[str] = None
    published_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    is_policy: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
