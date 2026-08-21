from app.utils.logger import Logger
from app.models.category import Category
from app.crud.data_crud.category import CategoryCRUD
from app.config.mysql_config import AsyncSessionLocal


class CategoryOperator:
    """
    插入

    调用示例：
        news_id = NewsOperator.insert_news(news_data)
        if news_id:
            print(f"新闻插入成功，ID: {news_id}")
    """

    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.category_curd = CategoryCRUD()

    async def insert_category(self, news_detail_data: Category):
        async with AsyncSessionLocal() as db:
            try:
                result = await self.category_curd.insert(db, news_detail_data)
                await db.commit()
                return result
            except Exception as e:
                print("[插入分类失败]:", e)
                await db.rollback()
                print("[回滚事务]")
                return None

    async def get_category_is_active(self) -> list[Category]:
        async with AsyncSessionLocal() as db:
            try:
                return await self.category_curd.get_category_is_active(db)
            except Exception as e:
                print("[获取有效分类失败]:", e)
                return []

    async def get_category_by_id(self, id: int) -> Category:
        async with AsyncSessionLocal() as db:
            try:
                return await self.category_curd.get(db, id)
            except Exception as e:
                print("[获取分类失败]:", e)
                return None
