from pydantic import BaseModel, Field
from typing import List

class NewsAnalysis(BaseModel):
    summary: str = Field(description="一句话速读")
    abstract: str = Field(description="3-5句话的详细摘要")
    topic_cluster: str = Field(description="Topic聚类")
    industry_category: str = Field(description="行业分类")
    keywords: List[str] = Field(description="关键词列表")
    policy_risk: dict = Field(description="政策/风险识别")