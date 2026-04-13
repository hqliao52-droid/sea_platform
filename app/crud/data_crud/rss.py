from app.crud.sea_data_base import BaseCRUD
from app.models.rss_source import RssSource

class RssSourceCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(RssSource)

rss_source_crud = RssSourceCRUD()