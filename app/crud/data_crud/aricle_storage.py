from app.crud.sea_data_base import BaseCRUD
from app.models.article_storage import ArticleStorage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class CategoryCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(ArticleStorage)

    async def get_by_id(self, db: AsyncSession, obj_id: int) -> ArticleStorage | None:
        return await self.get(db, obj_id)

    async def get_by_article_name(
        self, db: AsyncSession, article_name: str
    ) -> ArticleStorage | None:
        try:
            stmt = select(ArticleStorage).where(
                ArticleStorage.article_name == article_name
            )
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            print(f"[获取文章失败] {article_name} | 错误：{str(e)[:50]}")
            return None
