from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from typing import Any

from app.config.settings import settings


class DeepSeekReasoningContentMixin:
    """DeepSeek 请求补丁，保留 thinking mode 工具调用所需的思考内容。"""

    def _get_request_payload(
        self,
        input_: Any,
        *,
        stop: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """构造 DeepSeek 请求体，并回填 assistant 消息的 reasoning_content。"""
        payload = super()._get_request_payload(input_, stop=stop, **kwargs)
        messages = self._convert_input(input_).to_messages()
        payload_messages = payload.get("messages")
        if not isinstance(payload_messages, list):
            return payload

        for source_message, payload_message in zip(messages, payload_messages):
            if not isinstance(source_message, AIMessage) or not isinstance(
                payload_message, dict
            ):
                continue
            # DeepSeek thinking mode 中，带工具调用的 assistant 消息在后续请求里
            # 必须原样带回 reasoning_content，否则工具结果续跑会被服务端拒绝。
            reasoning_content = source_message.additional_kwargs.get(
                "reasoning_content"
            )
            if reasoning_content is not None:
                payload_message["reasoning_content"] = reasoning_content
        return payload


class LLMConfig:
    def __init__(self):
        # 一次性初始化豆包（兼容 OpenAI 格式）
        pass

    async def get_chat_llm(self, streaming: bool = True) -> ChatOpenAI:
        return await ChatOpenAI(
            model=settings.LLM_MODEL_DouBaoSeedLite,
            api_key=settings.LLM_API_KEY_DouBaoSeedLite,
            base_url=settings.LLM_BASE_URL_DouBaoSeedLite,
            temperature=0.7,
            streaming=streaming,
        )

    async def category_llm(self):
        return await ChatOpenAI(
            model=settings.LLM_MODEL_DouBaoSeedLite,
            api_key=settings.LLM_API_KEY_DouBaoSeedLite,
            base_url=settings.LLM_BASE_URL_DouBaoSeedLite,
            temperature=0.1,
        )

    async def summary_llm(self):
        return await ChatOpenAI(
            model=settings.LLM_MODEL_DouBaoSeedLite,
            api_key=settings.LLM_API_KEY_DouBaoSeedLite,
            base_url=settings.LLM_BASE_URL_DouBaoSeedLite,
            temperature=0.7,
        )

    def create_agent(self):
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


llm_config = LLMConfig()
