from typing import List
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.sea_data_base import BaseCRUD
from app.models.chat_message import ChatMessage


class ChatMessageCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(ChatMessage)

    async def get_chat_message_by_id(self, db: AsyncSession, id: int) -> ChatMessage:
        return await self.get(db, id)

    async def get_chat_message_by_user_id(
        self, db: AsyncSession, user_id: int
    ) -> List[ChatMessage]:
        stmt = select(ChatMessage).where(ChatMessage.user_id == user_id)
        result = await db.execute(stmt)
        messages: List[ChatMessage] = result.scalars().all()
        return messages

    async def get_chat_message_by_session_id(
        self, db: AsyncSession, session_id: int
    ) -> List[ChatMessage]:
        stmt = select(ChatMessage).where(ChatMessage.session_id == session_id)
        result = await db.execute(stmt)
        messages: List[ChatMessage] = result.scalars().all()
        return messages

    async def get_chat_message_by_pre_id(
        self, db: AsyncSession, pre_id: int
    ) -> ChatMessage:
        stmt = select(ChatMessage).where(ChatMessage.pre_id == pre_id)
        result = await db.execute(stmt)
        message: ChatMessage = result.scalars().scalar_one_or_none()
        return message

    async def get_dialog_history(
        self, db: AsyncSession, user_id: int, session_id: int, current_id: int
    ) -> List[ChatMessage]:
        """上下文裁剪： 仅获取最近6轮的对话历史"""
        stmt = (
            select(
                ChatMessage.id,
                ChatMessage.role,
                ChatMessage.content,
                ChatMessage.llm_refer_data,
                ChatMessage.llm_refer_data_id,
                ChatMessage.message_type,
            )
            .where(
                ChatMessage.id < current_id,
                ChatMessage.user_id == user_id,
                ChatMessage.session_id == session_id,
                ChatMessage.is_deleted == 0,
                ChatMessage.status == "done",
            )
            .order_by(desc(ChatMessage.id))
            .limit(6)
        )
        result = await db.execute(stmt)
        messages: List[ChatMessage] = result.scalars().all()
        return messages
