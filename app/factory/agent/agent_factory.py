from pathlib import Path
from typing import Any
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langfuse import Langfuse
from pydantic import BaseModel

from app.config.settings import settings
from app.factory.callback.langfuse_callback import set_langfuse_client
from app.factory.base_factory import BaseFactory
from app.config.llm_config import DeepSeekReasoningContentMixin
from app.utils.utils import generate_id


class BuildAgentSchemas(BaseModel):
    user_id: int | str | None = None
    session_id: str | None = None
    trace_id: str | None = None
    
    attach: str | Path | None = None
    file_name: str | None = None

class AgentFactory(BaseFactory):
    def __init__(
        self,
        *,
        model: str | None = None,
        temperature: float | None = None,
    ):
        self.model = model or settings.BASE_MODEL or settings.LLM_BASE_MODEL_DEEPSEEK
        self.temperature = temperature or settings.TEMPERATURE
        self.langfuse_enabled = settings.LANGFUSE_ENABLED

    def create(self):
        kwargs = {
            "model": self.model,
            "temperature": self.temperature,
            "stream_usage": True,
        }
        api_key = settings.API_KEY or settings.LLM_API_KEY_DEEPSEEK
        if api_key:
            kwargs["api_key"] = api_key
        base_url = settings.BASE_URL or settings.LLM_BASE_URL_DEEPSEEK
        if base_url:
            kwargs["base_url"] = base_url
        if settings.SUPPORTED_THINKING and settings.THINKING_ENABLED:
            # thinking 参数只对显式声明支持的模型传递，避免普通模型拒绝未知字段。
            kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
            if settings.REASONING_EFFORT:
                kwargs["reasoning_effort"] = settings.REASONING_EFFORT
        if settings.ENABLED_PENALTY:
            # 惩罚因子
            kwargs["frequency_penalty"] = settings.FREQUENCY_PENALTY
            kwargs["presence_penalty"] = settings.PRESENCE_PENALTY

        if "deepseek" in self.model.lower():
            from langchain_deepseek import ChatDeepSeek

            return type(
                "ChatDeepSeek",
                (DeepSeekReasoningContentMixin, ChatDeepSeek),
                {},
            )(**kwargs)
        return ChatOpenAI(**kwargs)


    async def abuild_agent(
        self, 
        *,
        user_id: int | str | None = None,
        session_id: str | None = None,
        trace_id: str | None = None,
        attach: str | Path | None = None,
        file_name: str | None = None,
    ):
        pass
