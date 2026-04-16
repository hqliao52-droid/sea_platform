from .news_detail_response_schema import NewsDetailResponse
from pydantic import BaseModel, Field
from typing import List, Optional

class NewsDetailsPageSchema(BaseModel):
    result: Optional[List[NewsDetailResponse]] = Field(None, description="新闻列表")
    total: Optional[int] = Field(None, description="总页数")
    page: Optional[int] = Field(None, description="当前页码")
    page_size: Optional[int] = Field(None, description="每页数量")