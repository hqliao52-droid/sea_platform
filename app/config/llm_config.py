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



llm_config = LLMConfig()
