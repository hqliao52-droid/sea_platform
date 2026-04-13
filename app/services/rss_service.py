from app.models.rss_source import RssSource
from app.crud.data_crud.rss import rss_source_crud
from app.schemas.rss_shema import RssSchema


class RssSourceOperator:
    @staticmethod
    def get_all_rss_sources() -> list[RssSource]:
        """获取所有激活的 rss 源"""
        list = rss_source_crud.get_all_active()
        result = [RssSchema.from_orm(item) for item in list]
        return result

    @staticmethod
    def get_active_rss_sources() -> list[RssSource]:
        """获取所有的 rss 源"""
        list = rss_source_crud.get_all()
        result = [RssSchema.from_orm(item) for item in list]
        return result
