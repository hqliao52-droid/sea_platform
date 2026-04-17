from app.utils.logger import Logger
from app.models.news_details_model import NewsDetail
from app.crud.data_crud.news_detail import NewsDetailCRUD
from app.config.mysql_config import db_session

class NewsDetailOperator:
    """
    插入

    调用示例：
        news_id = NewsOperator.insert_news(news_data)
        if news_id:
            print(f"新闻插入成功，ID: {news_id}")
    """
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.news_detail_crud = NewsDetailCRUD()

    def insert_news_detail(self, news_detail_data: NewsDetail) -> int:
        db = db_session()
        try:
            result = self.news_detail_crud.insert(db,news_detail_data)
            return  result
        except Exception as e:
            self.logger.error(f"插入失败:{e}")
            db.rollback()
            return None
        finally:
            db.close()

    def get_pages_news(self,page: int, page_size: int) -> list[NewsDetail]:
        db = db_session()
        try:
            # 获取分页数据
            result = self.news_detail_crud.get_pages_news(db,page, page_size)
            self.logger.info(f"查询成功:{result}")
            return result
        except Exception as e:
            self.logger.error(f"查询失败:{e}")
            return {"status":500,"news_detail_list":None,"total":0}
        finally:
            db.close()
    
    def get_news_detail_by_id(self,id: int) -> NewsDetail:
        db = db_session()
        try:
            result = self.news_detail_crud.get_news_detail_by_id(db,id)
            self.logger.info(f"查询成功:{result}")
            return result
        except Exception as e:
            self.logger.error(f"查询失败:{e}")
            raise {"status":500,"news_detail":None}
        
        finally:
            db.close()
