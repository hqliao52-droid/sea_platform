import time,asyncio
from fastapi import APIRouter,WebSocket, WebSocketDisconnect
from fastapi.responses  import StreamingResponse
from typing import List
from uuid import uuid4
from datetime import datetime

from app.utils.result_response import Result
from app.utils.result_response import ResultCode
from app.services.chat_message_service import ChatMessageOperator
from app.schemas.chat_message.chat_message import ChatMessageSchema,ChatMsg
from app.services.chat_session_service import ChatSessionOperator
from app.services.news_detail_service import NewsDetailOperator
from app.models.chat_message import ChatMessage
from app.utils.logger import Logger
from app.tasks.ai_task import run_llm_task
from app.config.redis_config import redis_client


chat_message_router = APIRouter()
chat_msg = ChatMessageOperator()
chat_session = ChatSessionOperator()
news_detail = NewsDetailOperator()

logger = Logger.setup_logger(Logger.set_file_date())

@chat_message_router.get("/get_by_session_id",response_model = Result[List[ChatMessageSchema]])
async def get_by_session_id(session_id:int):
    """通过session id查用户历史消息"""
    try:
        chat_message = chat_msg.get_chat_message_by_session_id(session_id)
        result = [ChatMessageSchema.from_orm(item) for item in chat_message]
        logger.info(f"通过session_id:{session_id}查询用户历史消息成功")
        return Result.success(result)
    except Exception as e:
        logger.error(f"通过session_id:{session_id}查询用户历史消息失败，错误信息：{str(e)}")
        return Result.error(ResultCode.SYSTEM_ERROR)
    
@chat_message_router.put("/insert_message")
async def insert_message(req:ChatMsg):
    """发送对话 - 写入用户消息"""
    logger.info(f"当前({datetime.now}),客户发送销售：{req.news_ids}")
    task_id = str(uuid4())

    now_time = datetime.now()
    refer_data = []
    if req.news_ids:
        for id in req.news_ids:
            news = news_detail.get_news_detail_by_id(id)
            refer_data.append(news.title)

    user_message = ChatMessage()
    user_message.task_id = task_id
    user_message.role = "user"
    user_message.message_type = 1
    user_message.content = req.query
    user_message.user_id = req.user_id
    user_message.session_id = req.session_id
    user_message.created_time = now_time
    user_message.llm_refer_data = refer_data or None
    user_message.llm_refer_data_id = req.news_ids or None
    user_message.status = "done"
    user_msg = chat_msg.insert_chat_message(user_message)

    ai_message = ChatMessage()
    ai_message.task_id = task_id
    ai_message.role = "assistant"
    ai_message.message_type = 2
    ai_message.content = ""
    ai_message.user_id = req.user_id
    ai_message.pre_id = user_msg.id
    ai_message.session_id = req.session_id
    ai_message.status = "streaming"
    ai_message.created_time = now_time
    ai_msg = chat_msg.insert_chat_message(ai_message)

    update_time = {"update_time":now_time}
    chat_session.update_session(req.session_id,update_time)

    # 发送celery任务
    req_dict = req.model_dump() 
    run_llm_task.delay(task_id, ai_msg.id,user_msg.id, req_dict)

    return Result.success(data={"task_id":task_id,"ai_msg_id":ai_msg.id})


@chat_message_router.get("/chat_stream/{task_id}")
async def stream(task_id: str):
    async def event_generator():
        last_len = 0

        while True:
            content = redis_client.get_stream(task_id) or ""

            # 有新内容
            if len(content) > last_len:
                delta = content[last_len:]
                last_len = len(content)

                yield f"data: {delta}\n\n"

                # 结束
                if "[[END]]" in delta:
                    break

                if "[[ERROR]]" in delta:
                    break

            await asyncio.sleep(0.05)

    return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # 🔥 关键（Nginx）
            }
        )

@chat_message_router.websocket("/ws/chat/{task_id}")
async def ws_chat(websocket: WebSocket, task_id: str):
    await websocket.accept()

    last_len = 0

    try:
        while True:
            content = redis_client.get_stream(task_id) or ""

            if len(content) > last_len:
                delta = content[last_len:]
                last_len = len(content)

                await websocket.send_text(delta)

                if "[[END]]" in delta:
                    break

            await asyncio.sleep(0.05)

    except WebSocketDisconnect:
        print("客户端断开")