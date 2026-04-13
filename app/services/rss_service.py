from models.rss_source import RssSource
from database.mysql import db


class RssSourceOperator:
    @staticmethod
    def get_all_rss_sources() -> list[RssSource]:
        """获取所有 rss 源"""
        return db.query(RssSource).all()

    @staticmethod
    def get_active_rss_sources() -> list[RssSource]:
        """获取所有激活的 rss 源"""
        return db.query(RssSource).filter(RssSource.is_active == 1).all()

    @staticmethod
    def get_rss_source_by_name(name: str) -> RssSource:
        """根据名称获取 rss 源"""
        return db.query(RssSource).filter(RssSource.name == name).first()
