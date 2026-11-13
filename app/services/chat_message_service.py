from typing import List
from dataclasses import dataclass
from datetime import datetime

from app.models.chat_message import ChatMessage
from app.crud.data_crud.chat_message import ChatMessageCRUD
from app.config.pg_config import AsyncSessionLocal
from app.utils.log import logger
from app.utils.utils import load_json



class ChatMessageOperator:
    """聊天消息"""

    def __init__(self):
        self.chat_message_curd = ChatMessageCRUD()

    async def insert_chat_message(self, chat_message: ChatMessage) -> ChatMessage:
        async with AsyncSessionLocal() as db:
            try:
                obj = await self.chat_message_curd.insert(db, chat_message)
                await db.commit()
                return obj
            except Exception as e:
                logger.error(f"插入失败：{str(e)}")
                await db.rollback()
                return None

    async def get_chat_message_by_id(self, id: int):
        async with AsyncSessionLocal() as db:
            try:
                chat_message = await self.chat_message_curd.get(db, id)
                return chat_message
            except Exception as e:
                logger.error(f"操作失败：{str(e)}")
                return None

    async def get_chat_message_by_pre_id(self, pre_id: int) -> ChatMessage:
        async with AsyncSessionLocal() as db:
            try:
                chat_message = await self.chat_message_curd.get_chat_message_by_pre_id(
                    db, pre_id
                )
                return chat_message
            except Exception as e:
                logger.error(f"操作失败：{str(e)}")
                return None

    async def get_chat_message_by_session_id(
        self, session_id: int
    ) -> List[ChatMessage]:
        async with AsyncSessionLocal() as db:
            try:
                chat_message = (
                    await self.chat_message_curd.get_chat_message_by_session_id(
                        db, session_id
                    )
                )
                return chat_message
            except Exception as e:
                logger.error(f"操作失败：{str(e)}")
                return None

    async def get_chat_message_by_user_id(self, user_id: int) -> List[ChatMessage]:
        async with AsyncSessionLocal() as db:
            try:
                chat_message = await self.chat_message_curd.get_chat_message_by_user_id(
                    db, user_id
                )
                return chat_message
            except Exception as e:
                logger.error(f"操作失败：{str(e)}")
                return None

    async def get_dialog_history(
        self, user_id, session_id, current_id
    ) -> List[ChatMessage]:
        async with AsyncSessionLocal() as db:
            try:
                chat_message = await self.chat_message_curd.get_dialog_history(
                    db, user_id, session_id, current_id
                )
                logger.info(f"获取历史上下文成功：{chat_message}")
                return chat_message
            except Exception as e:
                logger.error(f"获取历史上下文失败：{e}")
                return None

    async def update_by_id(self, id: int, update_data: dict) -> bool:
        async with AsyncSessionLocal() as db:
            try:
                obj = await self.chat_message_curd.update(db, id, update_data)
                await db.commit()
                if obj is not None:
                    return True
                else:
                    return False
            except Exception as e:
                await db.rollback()
                logger.error(f"更新失败：{str(e)}")
                return False

class BuildChatMessage:

    def build_msg_data(
        self, 
        session_id: int | None = None,
        user_id: int | None = None,
        task_id: str | None = None,
        pre_id: int | None = None,
        role: str | None = None,
        status: str | None = None,
        message_type: int | None = None,
        content: str | None = None,
        llm_refer_data: dict = None,
        llm_refer_data_id: dict = None,
        user_rating: int | None = None,
        current_user_ip_info: str | None = None,
        user_feedback: str | None = None,
        is_deleted: int = 0,
        reasoning_content: str | None = None,
    ) -> ChatMessage:
        now_time = datetime.now()
        msg = ChatMessage()
        msg.session_id = session_id
        msg.user_id = user_id
        msg.task_id = task_id
        msg.pre_id = pre_id
        msg.role = role
        msg.status = status
        msg.message_type = message_type
        msg.content = content
        msg.llm_refer_data = load_json(llm_refer_data)
        msg.llm_refer_data_id = load_json(llm_refer_data_id)
        msg.user_rating = user_rating
        msg.current_user_ip_info = current_user_ip_info
        msg.user_feedback = user_feedback
        msg.created_time = now_time
        msg.is_deleted = is_deleted
        msg.reasoning_content = reasoning_content

        return msg
        
