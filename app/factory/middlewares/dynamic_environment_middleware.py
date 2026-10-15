from __future__ import annotations

from datetime import datetime
from typing import Awaitable, Callable

from langchain.agents.middleware.types import (
    AgentMiddleware,
    AgentState,
    ContextT,
    ModelRequest,
    ModelResponse,
    ResponseT,
)
from langchain_core.messages import HumanMessage



class DynamicEnvironmentMiddleware(AgentMiddleware[AgentState, ContextT, ResponseT]):
    """每次模型调用前注入运行时环境信息，避免 Agent 缓存固化动态值。"""

    def _format_prompt(self,) -> str:
        """格式化当前运行的动态环境信息。"""
        return f"""## Environment Information
- Today: {datetime.now().strftime("%Y-%m-%d")}
        """

    def _prepend_to_latest_user_message(self, messages: list, prompt: str) -> list:
        """把环境信息放到最新用户消息的第一段，减少 system prompt 动态变化。"""
        for index in range(len(messages) - 1, -1, -1):
            message = messages[index]
            if not isinstance(message, HumanMessage):
                continue
            patched_messages = list(messages)
            patched_messages[index] = self._prepend_to_user_message(message, prompt)
            return patched_messages
        return messages

    def _prepend_to_user_message(
        self, message: HumanMessage, prompt: str
    ) -> HumanMessage:
        """按用户消息内容类型前置环境信息。"""
        content = message.content
        if isinstance(content, str):
            return message.model_copy(update={"content": f"{prompt}\n\n{content}"})
        if isinstance(content, list):
            return message.model_copy(
                update={"content": [{"type": "text", "text": prompt}, *content]}
            )
        return message

    def modify_request(
        self,
        request: ModelRequest[ContextT],
    ) -> ModelRequest[ContextT]:
        """把动态环境信息前置到本次最新用户消息。"""
        prompt = self._format_prompt()
        messages = self._prepend_to_latest_user_message(request.messages, prompt)
        return request.override(messages=messages)

    def wrap_model_call(
        self,
        request: ModelRequest[ContextT],
        handler: Callable[[ModelRequest[ContextT]], ModelResponse[ResponseT]],
    ) -> ModelResponse[ResponseT]:
        """同步模型调用前注入动态环境信息。"""
        return handler(self.modify_request(request))

    async def awrap_model_call(
        self,
        request: ModelRequest[ContextT],
        handler: Callable[
            [ModelRequest[ContextT]],
            Awaitable[ModelResponse[ResponseT]],
        ],
    ) -> ModelResponse[ResponseT]:
        """异步模型调用前注入动态环境信息。"""
        return await handler(self.modify_request(request))
