from app.crud.sea_data_base import BaseCRUD
from app.models.rss_source import RssSource

class RssSourceCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(RssSource)
    
    def get_all_active(self):
        """获取所有 is_active=1 的新闻"""
        return self.db.query(self.model)\
                        .filter(self.model.is_active == 1)\
                        .all()

    def get_all(self):
        """获取所有 is_active=1 的新闻"""
        return self.db.query(self.model)\
                        .all()
    
    def get_by_url(self,url):
        """根据url获取"""
        return self.db.query(self.model)\
                        .filter(self.model.url == url)\
                        .first()


rss_source_crud = RssSourceCRUD()