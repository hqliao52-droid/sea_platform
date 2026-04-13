# app/schemas/rss_schema.py
from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Optional

class RssSchema(BaseModel):
    id: int
    name: str
    url: str
    category: Optional[str] = None
    is_active: int
    is_api_key: Optional[int] = None
    update_rate: Optional[int] = None
    hot_rate: Optional[float] = None
    source_score: Optional[float] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)