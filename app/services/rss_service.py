from app.models.rss_source import RssSource
from app.crud.data_crud.rss import RssSourceCRUD
from app.schemas.rss.rss_shema import RssSchema
from app.config.mysql_config import AsyncSessionLocal
from app.utils.logger import Logger


class RssSourceOperator:
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.rss_source_crud = RssSourceCRUD()

    async def get_active_rss_sources(self) -> list[RssSource]:
        """获取所有激活的 rss 源"""
        async with AsyncSessionLocal() as db:
            try:
                list = await self.rss_source_crud.get_all_active(db)
                result = [RssSchema.model_validate(item) for item in list]
                return result
            except Exception as e:
                print("[获取激活的rss源失败]:", e)
                return []

    async def get_all_rss_sources(self) -> list[RssSource]:
        """获取所有的 rss 源"""
        async with AsyncSessionLocal() as db:
            try:
                list = await self.rss_source_crud.get_all(db)
                result = [RssSchema.model_validate(item) for item in list]
                return result
            except Exception as e:
                print("[获取所有的rss源失败]:", e)
                return []

    async def get_rss_detail_by_url(self, url: str) -> RssSource | None:
        """根据url获取rss源详情"""
        async with AsyncSessionLocal() as db:
            try:
                result = await self.rss_source_crud.get_by_url(db, url)
                return RssSchema.model_validate(result)
            except Exception as e:
                print("[根据url获取rss源详情失败]:", e)
                return None

    async def get_by_id(self, id: int) -> RssSource | None:
        """根据id获取rss源详情"""
        async with AsyncSessionLocal() as db:
            try:
                result = await self.rss_source_crud.get(db, id)
                return RssSchema.model_validate(result)
            except Exception as e:
                print("[根据id获取rss源详情失败]:", e)
                return None
