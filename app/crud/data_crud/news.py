from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict

from app.crud.sea_data_base import BaseCRUD
from app.models.news_model import News


class NewsCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(News)

    async def get_pages_news(
        self, db: AsyncSession, page: int, page_size: int
    ) -> Dict[str, Any]:
        # 计算偏移量
        skip = (page - 1) * page_size

        # 查询分页数据
        try:
            stmt = (
                select(News)
                .filter(News.is_policy == 1)
                .order_by(News.published_at.desc())
                .offset(skip)
                .limit(page_size)
            )
            result = await db.execute(stmt)
            news_list = result.scalars().all()

            # 获取总条数
            count_stmt = select(func.count()).select_from(News)
            total = await db.scalar(count_stmt)
            print(f"[获取分页数据成功]: {news_list}")
            return {"total": total, "news_list": news_list, "status": 200}
        except Exception as e:
            return {"status": 500, "message": "服务器错误"}

    async def get_news_by_url(self, db: AsyncSession, url: str):
        try:
            stmt = select(News).filter(News.url == url)
            result = await db.execute(stmt)
            news = result.scalars().first()
            return news
        except Exception as e:
            print(f"[根据url获取news失败]: {str(e)}")
            return None

    async def get_news_by_id(self, db: AsyncSession, id: int):
        try:
            news = await db.get(News, id)
            return news
        except Exception as e:
            print(f"[根据id获取news失败]: {str(e)}")
            return None

    async def is_news_exits(self, db: AsyncSession, url: str, published_at) -> bool:
        try:
            stmt = select(News).filter(
                News.url == url, News.published_at == published_at
            )
            result = await db.execute(stmt)
            news = result.scalars().first()
            return news is not None
        except Exception as e:
            print(f"[判断news是否存在失败]: {str(e)}")
            return False
