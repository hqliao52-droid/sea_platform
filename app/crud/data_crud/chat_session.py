from typing import List
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.sea_data_base import BaseCRUD
from app.models.chat_session import ChatSession


class ChatSessionCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(ChatSession)

    async def get_chat_session_by_id(self, db: AsyncSession, id: int) -> ChatSession:
        return await self.get(db, id)

    async def get_chat_session_by_user_id(
        self, db: AsyncSession, user_id: int
    ) -> List[ChatSession]:
        stmt = (
            select(ChatSession)
            .where(ChatSession.user_id == user_id)
            .order_by(desc(ChatSession.update_time))
        )
        result = await db.execute(stmt)
        chat_sessions: ChatSession = result.scalars().all()
        return chat_sessions

    async def get_chat_session_by_llm_id(
        self, db: AsyncSession, llm_id: int
    ) -> List[ChatSession]:
        stmt = (
            select(ChatSession)
            .where(ChatSession.llm_id == llm_id)
            .order_by(desc(ChatSession.update_time))
        )
        result = await db.execute(stmt)
        chat_sessions: ChatSession = result.scalars().all()
        return chat_sessions

    async def get_new_chat_session_by_user_id(
        self, db: AsyncSession, user_id: int
    ) -> ChatSession:
        stmt = (
            select(ChatSession)
            .where(ChatSession.user_id == user_id)
            .order_by(desc(ChatSession.update_time))
        )
        result = await db.execute(stmt)
        chat_sessions: ChatSession = result.scalar().scalars_one_or_none()
        return chat_sessions
