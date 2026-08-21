from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.sea_data_base import BaseCRUD
from app.models.rss_source import RssSource


class RssSourceCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(model=RssSource)

    async def get_all_active(self, db: AsyncSession) -> list[RssSource]:
        """获取所有 is_active=1 的新闻"""
        try:
            stmt = select(self.model).where(self.model.is_active == 1)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            return []

    async def get_by_url(self, db: AsyncSession, url: str) -> RssSource:
        """根据url获取"""
        try:
            stmt = select(self.model).where(self.model.url == url)
            result = await db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            return None
