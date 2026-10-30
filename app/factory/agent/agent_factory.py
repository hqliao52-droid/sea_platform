from pathlib import Path
from typing import Any
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain.agents import create_agent
from deepagents import create_deep_agent
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph

from app.config.settings import settings
from app.factory.base_factory import BaseFactory
from app.factory.middlewares.middleware_factory import MiddlewareFactory
from app.factory.tools.tools_factory import ToolsFactory
from app.factory.subagents.subagents_factory import SubagentFactory
from app.factory.backend.backend_factory import BackendFactory
from app.services.chat_session_service import ChatSessionOperator
from app.rag.prompt.agent_prompt import prompt as agent_prompt


chat_session_operator = ChatSessionOperator()

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

class BuildAgentSchemas(BaseModel):
    user_id: int | str | None = None
    session_id: str | None = None
    trace_id: str | None = None
    
    attach: str | Path | None = None
    file_name: str | None = None

class AgentFactory(BaseFactory):
    """
    创建 agent 代理工厂
    """
    def __init__(
        self,
        *,
        model: str | None = None,
        temperature: float | None = None,
    ):
        self.model = model or settings.BASE_MODEL or settings.LLM_BASE_MODEL_DEEPSEEK
        self.temperature = temperature or settings.TEMPERATURE
        self.langfuse_enabled = settings.LANGFUSE_ENABLED or False
        self.middlewares_factory = MiddlewareFactory()
        self.tools_factory = ToolsFactory()
        self.subagents_factory = SubagentFactory()
        self.backend_factory = BackendFactory()

    def create(self, **_vars) -> ChatOpenAI:
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

        if _vars.get("streaming", False):
            # 兼容旧接口
            kwargs["streaming"] = _vars.get("streaming")

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
        chat_mode: str = "chat",
        checkpointer: BaseCheckpointSaver | AsyncPostgresSaver | None = None,
    ) -> CompiledStateGraph:
        model = self.create()
        tools = self.tools_factory.create()
        system_prompt = f"""
            {agent_prompt.safe_system_prompt()}\n
            {system_prompt}\n
        """

        if chat_mode == "chat":
            return create_agent(
                model=model,
                tools=tools,
                system_prompt=system_prompt,
                checkpointer=checkpointer,
            ).with_config({"recursion_limit": 1000})

        middlewares = self.middlewares_factory.create()
        subagents = self.subagents_factory.create()
        backend = self.backend_factory.create(settings.BACKEND_NAME)

        # if attach and file_name:
        #     with open(attach, "rb") as f:


        kwargs: dict = {
            "model": model,
            "tools": tools,
            "system_prompt": system_prompt,
            "subagents": subagents,
            "middleware": middlewares,
            "checkpointer": checkpointer,
            "backend": backend,
        }

        return create_deep_agent(**kwargs).with_config({"recursion_limit": 1000})
        