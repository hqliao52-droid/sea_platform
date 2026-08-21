from pydantic import Field, ConfigDict, BaseModel
from datetime import datetime
from typing import Optional


class UserPushCategoryWeightSchema(BaseModel):
    id: int = Field(None, description="主键ID")
    # push_config_id: int = Field(..., description="推送表ID")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    category_id: int = Field(None, description="分类ID")
    category_name: str = Field(None, description="分类名称")
    weight: float = Field(None, description="分类权重")
    updated_at: Optional[datetime] = Field(None, description="上次修改时间")

    model_config = ConfigDict(from_attributes=True)


class UserPushCategoryWeightResponseSchema(BaseModel):
    id: int = Field(None, description="主键ID")
    push_config_id: int = Field(..., description="推送表ID")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="上次修改时间")
    category_id: int = Field(..., description="分类ID")
    category_name: str = Field(..., description="分类名称")
    weight: int = Field(..., description="分类权重")

    model_config = ConfigDict(from_attributes=True)
