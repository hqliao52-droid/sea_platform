from typing import Any
from langchain_openai import ChatOpenAI

from app.config.settings import settings
from app.factory.base_factory import BaseFactory
from app.config.llm_config import DeepSeekReasoningContentMixin


class AgentFactory(BaseFactory):
    def __init__(
        self,
    ):
        pass

    def create(self):
        model = settings.BASE_MODEL or settings.LLM_BASE_MODEL_DeepSeek
        kwargs = {
            "model": model,
            "temperature": settings.TEMPERATURE,
            "stream_usage": True,
        }
        api_key = settings.API_KEY or settings.LLM_API_KEY_DeepSeek
        if api_key:
            kwargs["api_key"] = api_key
        base_url = settings.BASE_URL or settings.LLM_BASE_URL_DeepSeek
        if base_url:
            kwargs["base_url"] = base_url
        if settings.SUPPORTED_THINKING and settings.THINKING_ENABLED:
            # thinking 参数只对显式声明支持的模型传递，避免普通模型拒绝未知字段。
            kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
            if settings.REASONING_EFFORT:
                kwargs["reasoning_effort"] = settings.REASONING_EFFORT
        if "deepseek" in model.lower():
            from langchain_deepseek import ChatDeepSeek

            return type(
                "ChatDeepSeek",
                (DeepSeekReasoningContentMixin, ChatDeepSeek),
                {},
            )(**kwargs)
        return ChatOpenAI(**kwargs)


    def build_agent(self, ):
        pass