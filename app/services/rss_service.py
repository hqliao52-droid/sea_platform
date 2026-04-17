from app.models.rss_source import RssSource
from app.crud.data_crud.rss import RssSourceCRUD
from app.schemas.rss_shema import RssSchema
from app.config.mysql_config import db_session
from app.utils.logger import Logger


class RssSourceOperator:
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.rss_source_crud = RssSourceCRUD()

    def get_active_rss_sources(self) -> list[RssSource]:
        """获取所有激活的 rss 源"""
        db = db_session()
        try:
            list = self.rss_source_crud.get_all_active(db)
            result = [RssSchema.from_orm(item) for item in list]
            return result
        except Exception as e:
            raise e
        finally:
            db.close()

    def get_all_rss_sources(self) -> list[RssSource]:
        """获取所有的 rss 源"""
        db = db_session()
        try:
            list = self.rss_source_crud.get_all(db)
            result = [RssSchema.from_orm(item) for item in list]
            return result
        except Exception as e:
            raise e
        finally:
            db.close()

    def get_rss_by_url(self,url:str)-> RssSource:
        """根据url获取rss源详情"""
        db = db_session()
        try:
            result = self.rss_source_crud.get_by_url(db,url)
            return RssSchema.from_orm(result)
        except Exception as e:
            raise e
        finally:
            db.close()
