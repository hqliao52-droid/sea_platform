from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from typing import List
from app.schemas.user_push_notify_channel.user_push_notify_channel_schema import (
    UserPushNotifyChannelSchema,
    UserPushNotifyChannelResponseSchema,
)
from app.schemas.user_push_category_wegiht.user_push_category_wegiht_schema import (
    UserPushCategoryWeightSchema,
    UserPushCategoryWeightResponseSchema,
)


class UserPushConfigSchema(BaseModel):
    # id:int = Field(None, description="主键ID")
    user_id: int = Field(None, description="分类ID")
    max_push_amount: int = Field(None, description="分类名称")
    is_enabled: int = Field(None, description="分类权重")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    weights: List[UserPushCategoryWeightSchema] = Field(
        default_factory=list,
        description="分类权重列表",
    )
    channels: List[UserPushNotifyChannelSchema] = Field(
        default_factory=list,
        description="通知渠道列表",
    )

    class Config:
        # 允许 ORM 对象直接转换为 Schema
        from_attributes = True


class UserPushConfigResponseSchema(BaseModel):
    id: int = Field(None, description="主键ID")
    user_id: int = Field(None, description="分类ID")
    max_push_amount: int = Field(None, description="分类名称")
    is_enabled: int = Field(None, description="分类权重")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    weights: List[UserPushCategoryWeightResponseSchema] = Field(
        default_factory=list,
        description="分类权重列表",
    )
    channels: List[UserPushNotifyChannelResponseSchema] = Field(
        default_factory=list,
        description="通知渠道列表",
    )

    class Config(ConfigDict):
        from_attributes = True
