from app.utils.logger import Logger
from app.models.chat_message import ChatMessage
from app.crud.data_crud.chat_message import ChatMessageCRUD
from app.config.mysql_config import AsyncSessionLocal
from typing import List


class ChatMessageOperator:
    """聊天消息"""

    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.chat_message_curd = ChatMessageCRUD()

    async def insert_chat_message(self, chat_message: ChatMessage) -> ChatMessage:
        async with AsyncSessionLocal() as db:
            try:
                obj = await self.chat_message_curd.insert(db, chat_message)
                await db.commit()
                return obj
            except Exception as e:
                await db.rollback()
                self.logger.error(e)
                return None

    async def get_chat_message_by_id(self, id: int):
        async with AsyncSessionLocal() as db:
            try:
                chat_message = await self.chat_message_curd.get(db, id)
                return chat_message
            except Exception as e:
                self.logger.error(e)
                return None

    async def get_chat_message_by_pre_id(self, pre_id: int) -> ChatMessage:
        async with AsyncSessionLocal() as db:
            try:
                chat_message = await self.chat_message_curd.get_chat_message_by_pre_id(
                    db, pre_id
                )
                return chat_message
            except Exception as e:
                self.logger.error(e)
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
                self.logger.error(e)
                return None

    async def get_chat_message_by_user_id(self, user_id: int) -> List[ChatMessage]:
        async with AsyncSessionLocal() as db:
            try:
                chat_message = await self.chat_message_curd.get_chat_message_by_user_id(
                    db, user_id
                )
                return chat_message
            except Exception as e:
                self.logger.error(e)
                return None

    async def get_dialog_history(
        self, user_id, session_id, current_id
    ) -> List[ChatMessage]:
        async with AsyncSessionLocal() as db:
            try:
                chat_message = await self.chat_message_curd.get_dialog_history(
                    db, user_id, session_id, current_id
                )
                self.logger.info(f"获取历史上下文成功：{chat_message}")
                return chat_message
            except Exception as e:
                self.logger.error(f"获取历史上下文失败：{e}")
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
                self.logger.error(f"更新失败：{str(e)}")
                return False
