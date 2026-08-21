from app.utils.logger import Logger
from app.config.mysql_config import AsyncSessionLocal
from app.models.news_model import News
from app.crud.data_crud.news import NewsCRUD


class NewsOperator:
    """
    插入

    调用示例：
        news_id = NewsOperator.insert_news(news_data)
        if news_id:
            print(f"新闻插入成功，ID: {news_id}")
    """

    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.news_crud = NewsCRUD()

    async def get_news_by_id(self, news_id: int):
        async with AsyncSessionLocal() as db:
            try:
                return await self.news_crud.get_news_by_id(db, news_id)
            except Exception as e:
                self.logger.error(f"查询失败:{e}")
                return None

    async def get_pages_news(self, page: int, page_size: int) -> list[News]:
        async with AsyncSessionLocal() as db:
            try:
                # 获取分页数据
                return await self.news_crud.get_pages_news(db, page, page_size)
            except Exception as e:
                self.logger.error(f"查询失败:{e}")
                return {"status": 500, "news_list": None, "total": 0}

    async def insert_news(self, news: News):
        async with AsyncSessionLocal() as db:
            try:
                await db.add(news)
                await db.commit()
                await db.refresh(news)
                return {"id": news.id, "status": "success"}
            except Exception as e:
                await db.rollback()
                return {"id": None, "status": "fail", "error": str(e)}

    async def is_news_exits(self, url: str, published_at) -> dict:
        async with AsyncSessionLocal() as db:
            try:
                result = self.news_crud.is_news_exits(db, url, published_at)

                if result:
                    return {"id": result[0], "status": "exists"}

                return {"id": None, "status": "NotExists"}
            except Exception as e:
                self.logger.error(f"查询失败:{e}")
                return {"id": None, "status": "fail", "error": str(e)}
