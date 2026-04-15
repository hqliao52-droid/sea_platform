from pydantic import BaseModel, Field
from typing import List, Optional

class NewsResponse(BaseModel):
    id: Optional[int] = Field(None, description="新闻ID")
    title: Optional[str] = Field(None, description="新闻标题")
    data_source: Optional[str] = Field(None, description="数据来源")
    is_policy: Optional[int] = Field(None, description="是否政策有关")
    url: Optional[str] = Field(None, description="新闻URL")
    published_at: Optional[str] = Field(None, description="发布时间")

    ai_summary: Optional[str] = Field(None, description="AI摘要（一句话速读）")
    one_sentence_summary: Optional[str] = Field(None, description="一句话速读")
    topic_cluster: Optional[str] = Field(None, description="Topic聚类")
    industry_category: Optional[str] = Field(None, description="行业分类")
    keywords: Optional[List[str]] = Field(None, description="关键词列表")
    policy_risk: Optional[dict] = Field(None, description="政策/风险识别")
    policy_compliance: Optional[dict] = Field(None, description="合规性识别")

    rss_tag: Optional[str] = Field(None, description="RSS标签/RSS名称")
    rss_id: Optional[int] = Field(None, description="RSS源ID")