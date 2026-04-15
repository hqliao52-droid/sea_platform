from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# --- 基础 Schema ---
class categoryBase(BaseModel):
    id: Optional[int] = Field(None, description="主键ID")
    tag_name: Optional[str] = Field(None, description="类名")
    example: Optional[str] = Field(None, description="标签示例")
    is_active: Optional[bool] = Field(None, description="启用状态")

    model_config = ConfigDict(from_attributes=True)