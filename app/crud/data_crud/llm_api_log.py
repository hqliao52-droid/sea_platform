from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.sea_data_base import BaseCRUD
from app.models.llm_api_log import LlmApiLog


class LlmApiLogCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(LlmApiLog)

    async def get_llm_api_log_by_id(self, db: AsyncSession, id: int) -> LlmApiLog:
        return await self.get(db, id)

    async def get_llm_api_log_by_session_id(
        self, db: AsyncSession, session_id: int
    ) -> List[LlmApiLog]:
        stmt = select(LlmApiLog).where(LlmApiLog.session_id == session_id)
        result = await db.execute(stmt)
        llm_api_log: List[LlmApiLog] = result.scalars().all()
        return llm_api_log

    async def get_llm_api_log_by_message_id(
        self, db: AsyncSession, message_id: int
    ) -> LlmApiLog:
        stmt = select(LlmApiLog).where(LlmApiLog.message_id == message_id)
        result = await db.execute(stmt)
        llm_api_log: LlmApiLog = result.scalars().first()
        return llm_api_log

    async def get_llm_api_log_by_model_name(
        self, db: AsyncSession, model_name: str
    ) -> List[LlmApiLog]:
        stmt = select(LlmApiLog).where(LlmApiLog.model_name == model_name)
        result = await db.execute(stmt)
        llm_api_log: List[LlmApiLog] = result.scalars().all()
        return llm_api_log
