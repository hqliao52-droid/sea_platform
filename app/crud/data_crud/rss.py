from app.crud.sea_data_base import BaseCRUD
from app.models.rss_source import RssSource
from app.config.mysql_config import db_session
from sqlalchemy.orm import Session

class RssSourceCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(RssSource)
    
    def get_all_active(self,db: Session):
        """获取所有 is_active=1 的新闻"""
        return db.query(self.model)\
                        .filter(self.model.is_active == 1)\
                        .all()

    
    def get_by_url(self,db:Session,url):
        """根据url获取"""
        return db.query(self.model)\
                        .filter(self.model.url == url)\
                        .first()


rss_source_crud = RssSourceCRUD()