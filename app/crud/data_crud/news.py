from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, Optional

from app.crud.sea_data_base import BaseCRUD
from app.models.news_model import News
from app.utils.time_convert import to_datetime


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

    async def get_news_by_url(self, db: AsyncSession, url: str) -> Optional[News]:
        try:
            stmt = select(News).filter(News.url == url)
            result = await db.execute(stmt)
            news = result.scalars().first()
            return news
        except Exception as e:
            print(f"[根据url获取news失败]: {str(e)}")
            return None

    async def get_news_by_id(self, db: AsyncSession, id: int) -> Optional[News]:
        try:
            news = await db.get(News, id)
            return news
        except Exception as e:
            print(f"[根据id获取news失败]: {str(e)}")
            return None

    async def is_news_exits(
        self, db: AsyncSession, url: str, published_at
    ) -> Optional[News]:
        """
        按 url + 发布时间判断 news 是否已存在

        published_at 必须是 datetime：传字符串时 SQLAlchemy 会按 VARCHAR 绑定，
        PostgreSQL 会报 operator does not exist: timestamp ... = character varying。
        解析不出时间时退化为只按 url 去重。
        """
        try:
            filters = [News.url == url]

            published_at = to_datetime(published_at)
            if published_at is not None:
                filters.append(News.published_at == published_at)

            stmt = select(News).filter(*filters)
            result = await db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            print(f"[判断news是否存在失败]: {str(e)}")
            return None
