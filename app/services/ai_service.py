import json
from typing import AsyncGenerator
from langchain_core.prompts import ChatPromptTemplate
from langchain.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from app.factory.agent.agent_factory import AgentFactory
from app.config.langgraph_postgres import create_checkpointer
from app.utils.log import logger
from app.config.llm_config import llm_config
from app.rag.prompt.agent_prompt import prompt as agent_prompt
from app.utils.utils import extract_content_stream, SSEEvent
from app.models.user_model import UserModel
from app.schemas.request.chat_request import ChatRequest
from app.services.chat_message_service import ChatMessageOperator
from app.models.chat_message import ChatMessage

class AIService:
    def __init__(self):
        self.llm_normal = llm_config.get_model(streaming=True)
        self.chat_service = ChatMessageOperator()

    async def build_history(self, session_id: int) -> list:
        history_messages = []
        msgs = await self.chat_service.get_chat_message_by_session_id(session_id)
        for item in msgs:
            msg = item.content
            role = item.role

            if not msg:
                continue
            match role:
                case "user":
                    history_messages.append(HumanMessage(msg))
                case "assistant":
                    history_messages.append(AIMessage(msg))
                # case "system":
                #     history_messages.append(SystemMessage(msg))
                case _:
                    continue

        return history_messages

    async def chat_ai_test(self, request: ChatRequest, user: UserModel) -> AsyncGenerator[str, None]:
        try:
            user_msg = ChatMessage(
                session_id=request.session_id,
                content=request.query,
                role="user",
                user_id=user.id,
                message_type=1,
                status="done"
            )
            # 先入库用户消息
            insert_user_msg: ChatMessage = await self.chat_service.insert_chat_message(user_msg)
            msgs = await self.build_history(request.session_id)
            msgs.append(SystemMessage(content=agent_prompt.base_service_system_prompt()))
            msgs.append(HumanMessage(content=request.query))

            prompt = ChatPromptTemplate.from_messages(msgs)

            chain = prompt | self.llm_normal

            buffer = ""
            async def text_generator() -> AsyncGenerator[str, None]:
                nonlocal buffer
                async for chunk in chain.astream({"query": request.query}):
                    if chunk.content:
                        buffer += chunk.content
                        result = json.dumps(
                            {
                                "content": chunk.content,
                            },
                            ensure_ascii=False,
                        )
                        yield result

            async for ev in extract_content_stream(
                text_generator(),
            ):
                yield SSEEvent.delta(field="content", content=ev)

            logger.info(f"chat ai返回：{buffer}")
            ai_msg = ChatMessage(
                session_id=request.session_id,
                content=buffer,
                role="assistant",
                user_id=user.id,
                message_type=2,
                status="done",
                pre_id=insert_user_msg.id if insert_user_msg else None
            )
            await self.chat_service.insert_chat_message(ai_msg)
        except Exception as e:
            logger.error(f"chat ai error: {e}")

            

    async def run_chat(query: str, user: UserModel) -> AsyncGenerator:
        checkpointer = create_checkpointer()

        agent = AgentFactory().abuild_agent()


ai_service = AIService()
