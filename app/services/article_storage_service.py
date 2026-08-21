from typing import Any

from app.utils.logger import Logger
from app.models.article_storage import ArticleStorage
from app.crud.data_crud.aricle_storage import CategoryCRUD as ArticleStorageCRUD
from app.config.mysql_config import AsyncSessionLocal


class ArticleStorageService:
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.category_curd = ArticleStorageCRUD()

    async def insert_article(self, article: ArticleStorage) -> dict[Any]:
        """
        插入文章
        """
        async with AsyncSessionLocal() as db:
            try:
                result = await self.category_curd.insert(db, article)
                await db.commit()
                return {"id": result.id, "status": "success"}
            except Exception as e:
                await db.rollback()
                return {"id": None, "status": "fail", "error": str(e)}

    async def get_by_article_name(self, article_name: str) -> ArticleStorage:
        """
        通过文章名称获取文章
        """
        async with AsyncSessionLocal() as db_session:
            result = await self.category_curd.get_by_article_name(
                db_session, article_name
            )
            return result
