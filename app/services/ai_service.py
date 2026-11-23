import json
from typing import AsyncGenerator, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    AIMessageChunk
)
from fastapi import WebSocket, Request
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.base import BaseCheckpointSaver

from app.factory.agent.agent_factory import AgentFactory
from app.factory.callback.langfuse_callback import set_langfuse_client, get_trace_id
from app.factory.tools.saved_news import search_saved_news, check_news_length_or_summary
from app.utils.utils import load_json
from app.config.llm_config import llm_config
from app.config.redis_config import redis_client
from app.rag.prompt.agent_prompt import prompt as agent_prompt
from app.schemas.request.chat_request import ChatRequest
from app.schemas.enum.ai_status import AIStatus, Role, MsgType
from app.schemas.chat_message.chat_message import ChatMsg
from app.services.chat_message_service import ChatMessageOperator, BuildChatMessage
from app.services.chat_session_service import ChatSessionOperator
from app.services.news_detail_service import NewsDetailOperator
from app.models.chat_message import ChatMessage
from app.models.user_model import UserModel
from app.models.news_details_model import NewsDetail
from app.utils.log import logger
from app.utils.utils import extract_content_stream, generate_id, SSEEvent

class AIService:
    def __init__(self):
        self.llm_normal = llm_config.get_model(streaming=True)
        self.chat_service = ChatMessageOperator()
        self.agent_factory = AgentFactory()
        self.chat_session_operator = ChatSessionOperator()
        self.langfuse_handler = [set_langfuse_client()]

    async def build_history(self, user_query: str | None, files: list[str] | None) -> list:
        history_messages = []
        if user_query:
            history_messages.append(HumanMessage(content=user_query))
        file_urls = []
        for file in (files or []):
            if not file.startswith(("http://", "https://")):
                raise ValueError("文件地址格式错误")
            file_urls.append({"type": "image_url", "image_url": {"url": file}})
        if file_urls:
            history_messages.append(HumanMessage(content=file_urls))
        return history_messages

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
        build_msg = BuildChatMessage()
        chat_msg = ChatMessageOperator()
        session_id = ""
        trace_id = None
        if request.session_id:
            session_id = request.session_id
            trace_id = await get_trace_id(request.user_id, request.session_id)
        else:
            session = await self.chat_session_operator.new_session(request.user_id)
            session_id = session.id
            trace_id = generate_id(is_32bit=True)
            await redis_client.set_trace_id(request.user_id, session.id, trace_id)

        user_msg = await chat_msg.insert_chat_message(
            build_msg.build_msg_data(
                session_id=session_id,
                role=Role.USER.value,
                user_id=request.user_id,
                message_type=MsgType.USER.value,
                content=request.query,
                llm_refer_data_id=request.news_ids,
                status=AIStatus.DONE.value
            )
        )
        user_query = request.query
        if request.news_ids:
            user_query += f"【引用了几篇材料：ids={request.news_ids}】"
        history_msgs = await self.build_history(user_query, request.files)
        system_prompt = agent_prompt.base_service_system_prompt()
        messages = {
            "messages": history_msgs
        }
        
        final_content = ""
        status = ""
        try:
            async def generator() -> AsyncGenerator[dict, None]:
                async for chunk in self.run_chat(
                    messages, 
                    system_prompt, 
                    app.app.state.checkpointer, 
                    has_other_tools=True,
                    trace_id=trace_id
                ):
                    yield chunk

            async for ev in generator():
                json_chunk = load_json(ev)
                if json_chunk.get("status") == AIStatus.GENERATING.value:
                    await websocket.send_json(json_chunk)
                elif json_chunk.get("status") == AIStatus.DONE.value:
                    final_content = json_chunk.get("final_content", "") 
                    status = json_chunk.get("status")
                else:
                    final_content = json_chunk.get("error_content", "")
                    status = json_chunk.get("status")
                    
        except Exception as e:
            logger.exception(str(e))
        finally:
            # 持久化AI消息
            await chat_msg.insert_chat_message(
                build_msg.build_msg_data(
                    session_id=session_id,
                    role=Role.ASSISTANT.value,
                    user_id=user_id,
                    message_type=MsgType.ASSISTANT.value,
                    content=final_content,
                    pre_id=user_msg.id,
                    status=status
                )
            )
            # 更新会话标题
            await self.run_llm_task_session_topic(session_id, request.query)
        

    async def test_chat(self, request: ChatMsg, app: Request, user: UserModel):
        trace_id = None
        try:
            if request.session_id:
                trace_id = await get_trace_id(user.id, request.session_id)
            else:
                session = await self.chat_session_operator.new_session(user.id)
                trace_id = generate_id(is_32bit=True)
                request.session_id = session.id
                await redis_client.set_trace_id(user.id, session.id, trace_id)
            history_msgs = await self.build_history(request.query, request.files)
            system_prompt = agent_prompt.base_service_system_prompt()
            messages = {
                "messages": history_msgs
            }
            try:
                async for chunk in self.run_chat(
                    messages, 
                    system_prompt, 
                    app.app.state.checkpointer, 
                    has_other_tools=True,
                    trace_id=trace_id
                ):
                    yield chunk
            except Exception as e:
                logger.exception(str(e))
                yield SSEEvent.error(code="500", message="Agent 异常")
        except Exception as e:
            logger.exception(str(e))
            await self.run_llm_task_session_topic(request.session_id, request.query)
            yield SSEEvent.error(code="500", message="Agent 异常")

    async def run_chat(
            self, 
            messages: dict, 
            system_prompt: str, 
            checkpointer: BaseCheckpointSaver | AsyncPostgresSaver | None = None,
            has_other_tools: bool = False,
            trace_id: str | None = None,
        ) -> AsyncGenerator:
        try:
            additional_tools = [search_saved_news, check_news_length_or_summary]
            agent = self.agent_factory.abuild_agent(
                chat_mode="chat", 
                system_prompt=system_prompt, 
                checkpointer=checkpointer,
                additional_tools=additional_tools if has_other_tools else []
            )
            agent_config: dict[str, Any] = {
                "callbacks": self.langfuse_handler,
                "metadata": {
                    "langfuse_session_id": trace_id,
                },
                "configurable": {
                    "thread_id": trace_id
                }
            }
            final_content = ""
            usage_data = {}
            tool_acc: AIMessageChunk | None = None
            tool_acc_id: str | None = None
            async for stream_mode, chunk in agent.astream(
                messages, 
                config=agent_config,
                stream_mode=["messages", "custom"]
            ):
                if not (chunk and isinstance(chunk, tuple)):
                    continue

                chunk_msg = chunk[0]
                match chunk_msg:
                    case AIMessageChunk():
                        if tool_acc_id != chunk_msg.id:
                            tool_acc, tool_acc_id = chunk_msg, chunk_msg.id
                        else:
                            tool_acc = tool_acc + chunk_msg
                        role = Role.ASSISTANT.value
                        reasoning = chunk_msg.additional_kwargs.get("reasoning_content")
                        if reasoning:
                            yield {
                                "role": role,
                                "content": chunk_msg.additional_kwargs.get("reasoning_content"),
                                "trace_id": trace_id,
                                "usage_metadata": usage_data,
                                "status": AIStatus.ANALYZING.value
                            }
                            continue
                        if chunk_msg.chunk_position == "last" and tool_acc.tool_calls:
                            for tc in tool_acc.tool_calls:
                                yield {
                                    "role": Role.TOOLS.value,
                                    "content": "",
                                    "tool_calls": [{"id": tc["id"], "name": tc["name"], "args": tc["args"]}],
                                    "trace_id": trace_id,
                                    "usage_metadata": usage_data,
                                    "status": AIStatus.RETRIEVING.value
                                }
                            continue
                        content = chunk_msg.content
                        usage_data = getattr(chunk_msg, "usage_metadata", {})
                        
                        if role == "assistant":
                            final_content += content
                        result = {
                            "role": role,
                            "content": content,
                            "trace_id": trace_id,
                            "usage_metadata": usage_data,
                            "status": AIStatus.GENERATING.value
                        }
                        yield result
                    case _:
                        role = "unknown"
        except Exception as e:
            logger.exception(str(e))
            yield {
                "status": AIStatus.EXCEPTION.value,
                "error_content": str(e),
                "trace_id": trace_id
            }
        finally:
            yield {
                "status": AIStatus.DONE.value,
                "final_content": final_content,
                "trace_id": trace_id
            }

    async def stream(self) -> AsyncGenerator:
        pass


ai_service = AIService()
