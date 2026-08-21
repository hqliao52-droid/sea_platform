from app.utils.logger import Logger
from app.models.chat_session import ChatSession
from app.schemas.chat_session.chat_session import ChatSessionSchema
from app.crud.data_crud.chat_message import ChatMessageCRUD
from app.crud.data_crud.chat_session import ChatSessionCRUD
from app.config.mysql_config import AsyncSessionLocal
from typing import List
from sqlalchemy.orm import Session


class ChatSessionOperator:
    """会话窗口操作类"""

    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.chat_session_curd = ChatSessionCRUD()
        self.chat_message_curd = ChatMessageCRUD()

    async def get_chat_session_by_id(self, id: int) -> ChatSessionSchema:
        async with AsyncSessionLocal() as db:
            try:
                chat_session = await self.chat_session_curd.get(db, id)
                chat_session_result = ChatSessionSchema.from_orm(chat_session)
                return chat_session_result
            except Exception as e:
                self.logger.error(e)
                return None

    async def get_chat_session_by_llm_id(self, llm_id: int) -> List[ChatSessionSchema]:
        async with AsyncSessionLocal() as db:
            try:
                chat_session = await self.chat_session_curd.get_chat_session_by_llm_id(
                    db, llm_id
                )
                chat_session_result = [
                    ChatSessionSchema.from_orm(item) for item in chat_session
                ]
                return chat_session_result
            except Exception as e:
                self.logger.error(e)
                return None

    async def get_chat_session_by_user_id(
        self, user_id: int
    ) -> List[ChatSessionSchema]:
        async with AsyncSessionLocal() as db:
            try:
                chat_session = await self.chat_session_curd.get_chat_session_by_user_id(
                    db, user_id
                )
                chat_session_result = [
                    ChatSessionSchema.from_orm(item) for item in chat_session
                ]
                return chat_session_result
            except Exception as e:
                self.logger.error(e)
                return None

    async def new_session(self, user_id: int) -> ChatSessionSchema:
        async with AsyncSessionLocal() as db:
            try:
                new_session = ChatSession(
                    user_id=user_id, llm_id=1, session_topic="新会话"
                )
                chat_session_result = await self.chat_session_curd.insert(
                    db, new_session
                )
                await db.commit()
                self.logger.info(f"新的会话创建成功：{chat_session_result}")
                return ChatSessionSchema.from_orm(chat_session_result)
            except Exception as e:
                self.logger.error(e)
                return None

    async def get_new_chat_session_by_user_id(self, user_id: int) -> ChatSessionSchema:
        async with AsyncSessionLocal() as db:
            try:
                chat_session = (
                    await self.chat_session_curd.get_new_chat_session_by_user_id(
                        db, user_id
                    )
                )
                if chat_session:  # 存在会话，进一步查询该会话是否为空消息
                    has_msg = (
                        await self.chat_message_curd.get_chat_message_by_session_id(
                            db, chat_session.id
                        )
                    )
                    if not has_msg:  # 空会话，直接返回该会话信息
                        return ChatSessionSchema.from_orm(chat_session)

                new_session = ChatSession(
                    user_id=user_id, llm_id=1, session_topic="新会话"
                )
                chat_session_result = await self.chat_session_curd.insert(
                    db, new_session
                )
                self.logger.info(f"新的会话创建成功：{chat_session_result}")

                await db.commit()
                return ChatSessionSchema.from_orm(chat_session_result)
            except Exception as e:
                await db.rollback()
                self.logger.error(e)
                return None

    async def update_session(self, session_id: int, session_data: dict):
        async with AsyncSessionLocal() as db:
            try:
                result = await self.chat_session_curd.update(
                    db, session_id, session_data
                )
                self.logger.info(f"更新会话成功：{result}")

                await db.commit()
                return result
            except Exception as e:
                await db.rollback()
                self.logger.error(f"更新失败：{str(e)}")
