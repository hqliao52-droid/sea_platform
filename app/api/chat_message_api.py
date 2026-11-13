import asyncio
from fastapi import (
    APIRouter, 
    WebSocket, 
    WebSocketDisconnect, 
    BackgroundTasks, 
    Request
)
from fastapi.responses import StreamingResponse
from typing import List
from uuid import uuid4
from datetime import datetime

from app.utils.result_response import Result
from app.utils.result_response import ResultCode
from app.services.chat_message_service import ChatMessageOperator, BuildChatMessage
from app.schemas.chat_message.chat_message import ChatMessageSchema, ChatMsg
from app.schemas.error.error_schemas import ValidationError
from app.services.chat_session_service import ChatSessionOperator
from app.services.news_detail_service import NewsDetailOperator
from app.services.ai_service import ai_service
from app.models.chat_message import ChatMessage
from app.utils.log import logger
from app.tasks.ai_task import run_llm_task
from app.config.redis_config import redis_client


chat_message_router = APIRouter()
chat_msg = ChatMessageOperator()
chat_session = ChatSessionOperator()
news_detail = NewsDetailOperator()


@chat_message_router.get(
    "/get_by_session_id", response_model=Result[List[ChatMessageSchema]]
)
async def get_by_session_id(session_id: int):
    """通过session id查用户历史消息"""
    try:
        chat_message = await chat_msg.get_chat_message_by_session_id(session_id)
        result = [ChatMessageSchema.model_validate(item) for item in chat_message]
        logger.info(f"通过session_id:{session_id}查询用户历史消息成功")
        return Result.success(result)
    except Exception as e:
        logger.error(
            f"通过session_id:{session_id}查询用户历史消息失败，错误信息：{str(e)}"
        )
        return Result.error(ResultCode.SYSTEM_ERROR)


@chat_message_router.put("/insert_message")
async def insert_message(
    req: ChatMsg,
    background_tasks: BackgroundTasks
    ):
    """发送对话 - 写入用户消息"""
    logger.info(f"当前({datetime.now}), 用户发送文章链接：{req.news_ids}")
    task_id = str(uuid4())

    now_time = datetime.now()
    refer_data = []
    if req.news_ids:
        for id in req.news_ids:
            news = await news_detail.get_news_detail_by_id(id)
            if news:
                refer_data.append(news.title)

    build_msg = BuildChatMessage()
    user_msg = await chat_msg.insert_chat_message(build_msg.build_msg_data(
            session_id=req.session_id,
            role = "user",
            user_id=req.user_id,
            task_id=task_id,
            message_type=1,
            content=req.query,
            llm_refer_data=refer_data,
            llm_refer_data_id=req.news_ids,
            status = "done"
        ))

    ai_msg = await chat_msg.insert_chat_message(build_msg.build_msg_data(
        session_id=req.session_id,
        role = "assistant",
        user_id=req.user_id,
        task_id=task_id,
        message_type=2,
        content="",
        pre_id=user_msg.id,
        status = "streaming"
    ))

    update_time = {"update_time": now_time}
    await chat_session.update_session(req.session_id, update_time)

    # 发送celery任务
    req_dict = req.model_dump()
    await asyncio.to_thread(run_llm_task.delay, task_id, ai_msg.id, user_msg.id, req_dict)
    background_tasks.add_task(
        ai_service.run_llm_task_session_topic, session_id=req.session_id, query=req.query
    )

    return Result.success(data={"task_id": task_id, "ai_msg_id": ai_msg.id})


@chat_message_router.get("/chat_stream/{task_id}")
async def stream(task_id: str):
    async def event_generator():
        last_len = 0

        while True:
            content = await redis_client.get_stream(task_id) or ""

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

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Nginx
        },
    )


@chat_message_router.websocket("/ws/chat/{task_id}")
async def ws_chat(websocket: WebSocket, task_id: str):
    await websocket.accept()

    last_len = 0

    try:
        while True:
            content = await redis_client.get_stream(task_id) or ""

            if len(content) > last_len:
                delta = content[last_len:]
                last_len = len(content)

                await websocket.send_text(delta)

                if "[[END]]" in delta:
                    break

    except WebSocketDisconnect as e:
        logger.error(f"/ws/chat/{task_id} 轮询接口出错：{str(e)}")
    finally:
        await websocket.close()

@chat_message_router.websocket("/ws/chat_with_ai")
async def ws_chat_with_ai(
    websocket: WebSocket, 
):
    await websocket.accept()
    try:
        req = ChatMsg.model_validate(await websocket.receive_json())
    except (WebSocketDisconnect, ValidationError):
        await websocket.close(code=1008, reason="invalid ChatMsg")
        return
    refer_data = []
    if req.news_ids:
        for id in req.news_ids:
            news = await news_detail.get_news_detail_by_id(id)
            if news:
                refer_data.append(news.title)

    build_msg = BuildChatMessage()
    user_msg = await chat_msg.insert_chat_message(build_msg.build_msg_data(
            session_id=req.session_id,
            role = "user",
            user_id=req.user_id,
            message_type=1,
            content=req.query,
            llm_refer_data=refer_data,
            llm_refer_data_id=req.news_ids,
            status = "done"
        ))

    try:
        await ai_service.websocket_stream(websocket, req, websocket, user_msg.id)
    except WebSocketDisconnect as e:
        logger.error(f"/ws/chat_with_ai 轮询接口出错：{str(e)}")
    finally:
        await websocket.close()
        now_time = datetime.now()
        update_time = {"update_time": now_time}
        await chat_session.update_session(req.session_id, update_time)