import json
from typing import AsyncGenerator, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    AIMessageChunk
)
from fastapi import WebSocket, Request
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.base import BaseCheckpointSaver

from app.factory.agent.agent_factory import AgentFactory
from app.factory.callback.langfuse_callback import set_langfuse_client, get_trace_id, set_trace_id
from app.config.llm_config import llm_config
from app.config.redis_config import redis_client
from app.rag.prompt.agent_prompt import prompt as agent_prompt
from app.schemas.request.chat_request import ChatRequest
from app.schemas.enum.ai_status import AIStatus, Role
from app.schemas.chat_message.chat_message import ChatMsg
from app.services.chat_message_service import ChatMessageOperator, BuildChatMessage
from app.services.chat_session_service import ChatSessionOperator
from app.models.chat_message import ChatMessage
from app.models.user_model import UserModel
from app.utils.log import logger
from app.utils.utils import extract_content_stream, generate_id, SSEEvent

class AIService:
    def __init__(self):
        self.llm_normal = llm_config.get_model(streaming=True)
        self.chat_service = ChatMessageOperator()
        self.agent_factory = AgentFactory()
        self.chat_session_operator = ChatSessionOperator()
        self.langfuse_handler = [set_langfuse_client()]
        self.trace_id = None

    async def build_history(self, session_id: int, files: list[str]) -> list:
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
                case "system":
                    history_messages.append(SystemMessage(msg))
                case _:
                    continue

        file_urls = []
        for file in (files or []):
            if not file.startswith(("http://", "https://")):
                raise ValueError("文件地址格式错误")
            file_urls.append({"type": "image_url", "image_url": {"url": file}})
        if file_urls:
            history_messages.append(HumanMessage(content=file_urls))
        return history_messages

    async def chat_ai_test(self, request: ChatRequest, user: UserModel) -> AsyncGenerator[str, None]:
        ai_done = False
        buffer = ""
        reasoning_content = ""
        try:
            yield SSEEvent.metadata(field="session_id", content=request.session_id)
            user_msg = ChatMessage(
                session_id=request.session_id,
                content=request.query,
                role=Role.USER.value,
                user_id=user.id,
                message_type=1,
                status=AIStatus.DONE.value,
            )
            msgs = await self.build_history(request.session_id, request.files)
            # 先入库用户消息
            insert_user_msg: ChatMessage = await self.chat_service.insert_chat_message(user_msg)
            msgs.append(SystemMessage(content=agent_prompt.base_service_system_prompt()))
            msgs.append(HumanMessage(content=request.query))
            prompt = ChatPromptTemplate.from_messages(msgs)

            chain = prompt | self.llm_normal

            async def text_generator() -> AsyncGenerator[str, None]:
                nonlocal buffer, reasoning_content
                async for chunk in chain.astream({"query": request.query}):
                    if chunk.additional_kwargs.get("reasoning_content", ""):
                        # 思考内容存档
                        reasoning = chunk.additional_kwargs.get("reasoning_content", "")
                        reasoning_content += reasoning
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

            logger.info(f"chat ai推理内容: {reasoning_content}")
            logger.info(f"chat ai返回：{buffer}")
            ai_done = True
        except Exception as e:
            logger.exception(e)
            ai_done = False
            yield SSEEvent.error(code="500", message="Agent 调用异常")
        finally:
            # 持久化AI消息
            ai_msg = ChatMessage(
                session_id=request.session_id,
                content=buffer,
                reasoning_content=reasoning_content,
                role=Role.ASSISTANT.value,
                user_id=user.id,
                message_type=2,
                status=AIStatus.DONE.value if ai_done else AIStatus.EXCEPTION.value,
                pre_id=insert_user_msg.id if insert_user_msg else None
            )
            await self.chat_service.insert_chat_message(ai_msg)

    def _message_to_dict(self, message: AIMessage) -> dict:
        """将 AIMessage 转换为可直接 JSON 序列化的字典"""
        return {
            "content": message.content,
            "additional_kwargs": message.additional_kwargs,
            "response_metadata": message.response_metadata,
            "id": message.id,
            "usage_metadata": getattr(message, "usage_metadata", None),
        }

    async def session_topic_generator(self, user_input: str):
        llm = llm_config.get_model()
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", agent_prompt.dialog_topic_prompt()),
                ("user", "{query}"),
            ]
        )
        chain = prompt | llm
        response: AIMessage = await chain.ainvoke({"query": user_input})
        data = self._message_to_dict(response)
        return data

    async def run_llm_task_session_topic(self, session_id: int, query: str):
        """判断当前会话是否为新会话，如果是，则更新会话主题"""
        try:
            chat_session = await self.chat_session_operator.get_chat_session_by_id(session_id)
            logger.info(f"会话信息: {chat_session}")
            if chat_session.session_topic == "新会话":
                session_topic = await self.session_topic_generator(query)
                logger.info(f"会话主题生成成功：{session_topic}")
                topic = {"session_topic": session_topic["content"]}
                obj = await self.chat_session_operator.update_session(session_id, topic)
                logger.info(f"会话主题更新：{obj}")
        except Exception as e:
            logger.error(f"会话主题更新失败：{str(e)}")
            raise e

    async def websocket_stream(self, websocket: WebSocket, request: ChatMsg, app: Request, user_id: int) -> None:
        if request.session_id:
            await self.run_llm_task_session_topic(request.session_id, request.query)
        else:
            session = await self.chat_session_operator.new_session(request.user_id)
            self.trace_id = generate_id(is_32bit=True)
            await redis_client.set_trace_id(request.user_id, session.id, self.trace_id)
        history_msgs = await self.build_history(request.session_id, request.files)
        system_prompt = agent_prompt.base_service_system_prompt()
        history_msgs.append(HumanMessage(content=request.query))
        messages = {
            "messages": history_msgs
        }
        build_msg = BuildChatMessage()
        chat_msg = ChatMessageOperator()
        try:
            async def generator() -> AsyncGenerator[dict, None]:
                async for chunk in self.run_chat(messages, system_prompt, app.app.state.checkpointer):
                    yield chunk
            async for ev in generator():
                json_chunk = json.dumps(ev, ensure_ascii=False)
                if json_chunk["status"] == "streaming":
                    await websocket.send_json(json_chunk)
                elif json_chunk["status"] == "done":
                    await chat_msg.insert_chat_message(build_msg.build_msg_data(
                        session_id=request.session_id,
                        role = "assistant",
                        user_id=user_id,
                        message_type=2,
                        content="",
                        pre_id=user_id,
                        status = "streaming"
                    ))
        except Exception as e:
            logger.exception(e)
        

    async def test_chat(self, request: ChatMsg, app: Request):
        try:
            if request.session_id:
                self.trace_id = await get_trace_id(request.user_id, request.session_id)
            else:
                session = await self.chat_session_operator.new_session(request.user_id)
                self.trace_id = generate_id(is_32bit=True)
                request.session_id = session.id
                await redis_client.set_trace_id(request.user_id, session.id, self.trace_id)
            history_msgs = await self.build_history(request.session_id, request.files)
            system_prompt = agent_prompt.base_service_system_prompt()
            history_msgs.append(HumanMessage(content=request.query))
            messages = {
                "messages": history_msgs
            }
            try:
                async for chunk in self.run_chat(messages, system_prompt, app.app.state.checkpointer):
                    yield chunk
            except Exception as e:
                logger.exception(e)
                yield SSEEvent.error(code="500", message="Agent 异常")
        except Exception as e:
            logger.exception(e)
            await self.run_llm_task_session_topic(request.session_id, request.query)
            yield SSEEvent.error(code="500", message="Agent 异常")

    async def run_chat(
            self, 
            messages: dict, 
            system_prompt: str, 
            checkpointer: BaseCheckpointSaver | AsyncPostgresSaver | None = None
        ) -> AsyncGenerator:
        try:
            agent = self.agent_factory.abuild_agent(
                chat_mode="chat", 
                system_prompt=system_prompt, 
                checkpointer=checkpointer
            )
            agent_config: dict[str, Any] = {
                "callbacks": self.langfuse_handler,
                "metadata": {
                    "langfuse_session_id": self.trace_id,
                },
                "configurable": {
                    "thread_id": self.trace_id
                }
            }
            final_content = ""
            usage_data = {}
            async for stream_mode, chunk in agent.astream(
                messages, 
                config=agent_config,
                stream_mode=["messages", "custom"]
            ):
                if chunk and isinstance(chunk, tuple):
                    chunk_msg = chunk[0]
                    if stream_mode == "custom":
                        role = "custom"
                    else:
                        match chunk_msg:
                            case AIMessageChunk():
                                role = "assistant"
                            case ToolMessage():
                                role = "tools"
                            case _:
                                role = "unknown"
                    try:
                        content = chunk_msg.content
                        usage_data = getattr(chunk_msg, "usage_metadata", {})
                        
                        if role == "assistant":
                            final_content += content
                        elif role == "tools":
                            pass
                        else:
                            pass
                        result = {
                            "role": role,
                            "content": content,
                            "trace_id": self.trace_id,
                            "usage_metadata": usage_data,
                            "status": "streaming"
                        }
                        yield result
                    except Exception as e:
                        logger.exception(e)
                logger.info({
                    "final_content": final_content,
                    "usage_metadata": usage_data,
                    "trace_id": self.trace_id
                })
        except Exception as e:
            logger.exception(e)
            yield {
                "status": "error",
                "content": final_content,
                "trace_id": self.trace_id
            }
        finally:
            yield {
                "status": "done",
                "content": final_content,
                "trace_id": self.trace_id
            }

    async def stream(self) -> AsyncGenerator:
        pass


ai_service = AIService()
