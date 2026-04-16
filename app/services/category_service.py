from app.utils.logger import Logger
from app.models.category import category
from app.crud.data_crud.category import CategoryCRUD
from app.config.mysql_config import db_session

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


    def insert_category(self, news_detail_data: category):
        db = db_session()
        try:
            result = self.category_curd.insert(db, news_detail_data)
            return result
        except Exception as e:
            db.rollback()   # ⭐ 必须
            raise e
        finally:
            db.close()      # ⭐ 必须
    
    def get_category_is_active(self) -> list[category]:
        db = db_session()
        try:
            return self.category_curd.get_category_is_active(db)
        except Exception as e:
            raise e
        finally:
            db.close()