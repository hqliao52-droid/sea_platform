from typing import Dict, Any, List, Optional
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.sea_data_base import BaseCRUD
from app.models.news_details_model import NewsDetail


class NewsDetailCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(NewsDetail)

    async def get_pages_news(
        self, db: AsyncSession, page: int = 1, page_size: int = 10
    ) -> Dict[str, Any]:
        """
        分页查询新闻
        :param db: 数据库会话
        :param page: 当前页码，从1开始
        :param page_size: 每页数量
        :return: 包含总数和新闻列表的字典
        """
        # 计算偏移量
        skip = (page - 1) * page_size

        # 查询分页数据（按发布时间倒序）
        count_stmt = select(func.count()).select_from(NewsDetail)
        total = await db.scalar(count_stmt)

        stmt = (
            select(NewsDetail)
            .order_by(desc(NewsDetail.published_at))
            .offset(skip)
            .limit(page_size)
        )
        result = await db.execute(stmt)
        news_list = result.scalars().all()

        return {
            "total": total or 0,
            "news_detail_list": news_list,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,  # 计算总页数
            "status": 200,
        }

    async def get_pages_news_by_category_id(
        self,
        db: AsyncSession,
        page: int = 1,
        page_size: int = 10,
        category_id: int = None,
    ) -> Dict[str, Any]:
        """
        分页查询新闻
        :param db: 数据库会话
        :param page: 当前页码，从1开始
        :param page_size: 每页数量
        :param category_id: 新闻分类ID
        :return: 包含总数和新闻列表的字典
        """
        # 计算偏移量
        skip = (page - 1) * page_size

        # 查询分页数据
        filters = []
        if category_id:
            filters.append(NewsDetail.category_id == category_id)

        count_stmt = select(func.count()).select_from(NewsDetail)

        if filters:
            count_stmt = count_stmt.where(*filters)
        total = await db.scalar(count_stmt) or 0

        stmt = select(NewsDetail)
        if filters:
            stmt = stmt.where(*filters)
        stmt = (
            stmt.order_by(desc(NewsDetail.published_at)).offset(skip).limit(page_size)
        )

        result = await db.execute(stmt)

        news_list = result.scalars().all()

        return {
            "total": total,
            "news_detail_list": news_list,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,  # 获取总页数
            "status": 200,
        }

    async def get_news_detail_by_id(
        self, db: AsyncSession, news_id: int
    ) -> Optional[NewsDetail]:
        """
        根据ID查询新闻
        :param db: 数据库会话
        :param news_id: 新闻ID
        :return: 新闻详情
        """
        stmt = select(NewsDetail).filter(NewsDetail.id == news_id)
        result = await db.execute(stmt)
        news_detail = result.scalars().first() or None
        return news_detail

    async def get_news_detail_by_ids(
        self, db: AsyncSession, news_ids: list[int]
    ) -> List[tuple]:
        """
        根据ID列表查询新闻
        :param db: 数据库会话
        :param news_ids: 新闻ID列表
        :return: 新闻详情列表
        """
        stmt = select(NewsDetail).filter(NewsDetail.id.in_(news_ids))
        result = await db.execute(stmt)
        news_details = result.scalars().all()
        return news_details
