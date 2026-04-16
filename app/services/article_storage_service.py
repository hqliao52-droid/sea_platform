from app.utils.logger import Logger
from app.models.article_storage import ArticleStorage
from app.crud.data_crud.aricle_storage import CategoryCRUD as ArticleStorageCRUD
from app.config.mysql_config import db_session

class ArticleStorageService:
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.category_curd = ArticleStorageCRUD()

    def insert_article(self,article:ArticleStorage):
        db = db_session()
        try:
            db.add(article)
            db.commit()
            db.refresh(article)
            return {"id":article.id,"status":"success"}
        except Exception as e:
            db.rollback()
            return {"id":None,"status":"fail","error":str(e)}
        finally:
            db.close()
    
    def get_by_article_name(self,article_name:str) -> ArticleStorage:
        db = db_session()
        try:
            result = self.category_curd.get_by_article_name(db,article_name)
            return result
        except Exception as e:
            raise e
        finally:
            db.close()
