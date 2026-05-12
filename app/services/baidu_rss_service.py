from app.utils.logger import Logger
from app.models.baidu_rss_source import BaiduRssSource
from app.crud.data_crud.baidu_rss_source import BaiduRssSourceCRUD
from app.config.mysql_config import db_session

class BaiduRssSourceOperator:
    """百度RSS源操作"""
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.baidu_rss_source_curd = BaiduRssSourceCRUD()

    def get_active_rss_sources(self) -> list[BaiduRssSource]:
        db = db_session()
        try:
            rss_sources = self.baidu_rss_source_curd.get_active_rss_sources(db)
            return rss_sources
        except Exception as e:
            self.logger.error(f"获取百度RSS源失败: {e}")
            return []
        finally:
            db.close()