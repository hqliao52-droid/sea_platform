from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class BaiduRssSourceSchema(BaseModel):
    """RSS数据源模型"""
    id: Optional[int] = Field(None, description="主键ID")
    name: Optional[str] = Field(None, description="目标网站名称")
    url: Optional[str] = Field(None, description="目标网站URL")
    category: Optional[str] = Field(None, description="目录")
    is_child: Optional[int] = Field(1, description="是否为子类rss")
    parent_id: Optional[int] = Field(None, description="父节点ID")
    is_active: Optional[int] = Field(1, description="是否可用 1:可用 0:不可用")
    is_api_key: Optional[int] = Field(0, description="是否需要API秘钥 1：是 0：否")
    update_rate: Optional[int] = Field(None, description="更新频率")
    hot_rate: Optional[float] = Field(None, description="热点率")
    source_score: Optional[float] = Field(None, description="综合分数")
    created_at: Optional[datetime] = Field(None, description="构建时间")

    model_config = ConfigDict(from_attributes=True)