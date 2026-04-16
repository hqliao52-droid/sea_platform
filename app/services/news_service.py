from app.utils.logger import Logger
from app.config.mysql_config import db_session
from app.models.news_model import News

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
    
    def get_news_by_id(self,news_id: int):
        from app.crud.data_crud.news import news_crud
        db = db_session()
        try:
            return news_crud.get(news_id)
        except Exception as e:
            self.logger.error(f"查询失败:{e}")
            return None
        finally:
            db.close()

    def get_pages_news(self,page: int, page_size: int) -> list[News]:
        from app.crud.data_crud.news import news_crud
        try:
            # 获取分页数据
            return news_crud.get_pages_news(page, page_size)
        except Exception as e:
            self.logger.error(f"查询失败:{e}")
            return {"status":500,"news_list":None,"total":0}


    def insert_news(self, news: News):
        db = db_session()
        try:
            db.add(news)
            db.commit()
            db.refresh(news)
            return {"id": news.id, "status": "success"}
        except Exception as e:
            db.rollback()
            return {"id": None, "status": "fail", "error": str(e)}
        finally:
            db.close()
    
    def is_news_exits(self, url: str, published_at):
        db = db_session()
        try:
            result = db.query(News.id).filter(
                News.url == url,
                News.published_at == published_at
            ).first()

            if result:
                return {"id": result[0], "status": "exists"}

            return {"id": None, "status": "NotExists"}
        finally:
            db.close()
            