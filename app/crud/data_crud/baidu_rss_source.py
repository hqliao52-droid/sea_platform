from app.crud.sea_data_base import  BaseCRUD
from app.models.baidu_rss_source import BaiduRssSource
from sqlalchemy.orm import Session


class BaiduRssSourceCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(BaiduRssSource)

    def get_active_rss_sources(self,db:Session) -> list[BaiduRssSource]:
        return db.query(BaiduRssSource).filter(BaiduRssSource.is_active==0).all()

    def get_by_url(self,db:Session,url:str) -> BaiduRssSource:
        return db.query(BaiduRssSource).filter(BaiduRssSource.url==url).first()