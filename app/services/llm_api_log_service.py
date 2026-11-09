from app.utils.log import logger
from app.models.llm_api_log import LlmApiLog
from app.crud.data_crud.llm_api_log import LlmApiLogCRUD
from app.config.pg_config import AsyncSessionLocal
from typing import List


class LlmApiLogOperator:
    """LLM API 调用日志记录"""

    def __init__(self):
        self.llm_api_log_curd = LlmApiLogCRUD()

    async def get_info_by_id(self, id: int) -> LlmApiLog:
        async with AsyncSessionLocal() as db:
            try:
                result = await self.llm_api_log_curd.get_llm_api_log_by_id(db, id)
                logger.info(f"查询成功:{result}")
                return result
            except Exception as e:
                logger.error(f"查询失败:{e}")
                return None

    async def get_info_by_message_id(self, message_id: int) -> LlmApiLog:
        async with AsyncSessionLocal() as db:
            try:
                result = await self.llm_api_log_curd.get_llm_api_log_by_message_id(
                    db, message_id
                )
                logger.info(f"查询成功:{result}")
                return result
            except Exception as e:
                logger.error(f"查询失败:{e}")
                return None

    async def get_info_by_model_name(self, model_name: str) -> List[LlmApiLog]:
        async with AsyncSessionLocal() as db:
            try:
                result = await self.llm_api_log_curd.get_llm_api_log_by_model_name(
                    db, model_name
                )
                logger.info(f"查询成功:{result}")
                return result
            except Exception as e:
                logger.error(f"查询失败:{e}")
                return None
