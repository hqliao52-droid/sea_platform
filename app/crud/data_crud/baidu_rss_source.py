from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.sea_data_base import BaseCRUD
from app.models.baidu_rss_source import BaiduRssSource


class BaiduRssSourceCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(model=BaiduRssSource)

    async def get_active_rss_sources(self, db: AsyncSession) -> list[BaiduRssSource]:
        stmt = select(BaiduRssSource).where(BaiduRssSource.is_active == 1)
        reult = await db.execute(stmt)
        rss_sources: list[BaiduRssSource] = reult.scalar().all()
        return rss_sources

    async def get_by_url(self, db: AsyncSession, url: str) -> BaiduRssSource:
        stmt = select(BaiduRssSource).where(BaiduRssSource.url == url)
        reult = await db.execute(stmt)
        rss_source: BaiduRssSource = reult.scalar_one_or_none()
        return rss_source
