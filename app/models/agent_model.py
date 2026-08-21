from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.utils import generate_id


class CommonBaseModel(BaseModel):
    trace_id: str = Field(
        default_factory=None,
        description="trace_id, 支持传入,否则为空",
    )
    model_config = ConfigDict(extra="allow")


class AgentModel(CommonBaseModel):
    agent: str | None = Field(..., description="agent名称")
    session_id: str | None = Field(
        default_factory=generate_id, description="会话的唯一标识"
    )
    message: str | None = Field(default="", description="用户输入的消息内容")
    stream: bool = Field(default=False, description="是否开启流式响应")
    files: list[dict] | None = Field(default_factory=list, description="上传的文件")

    prompt_params: dict | None = Field(
        default_factory=dict, description="自定义填充提示词"
    )

    @field_validator(session_id)
    def validator_session_id(cls, v) -> str:
        if not v:
            v = generate_id()
        return v
