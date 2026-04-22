from app.crud.sea_data_base import BaseCRUD
from app.models.news_details_model import NewsDetail
from typing import Dict, Any
from sqlalchemy.orm import Session

class NewsDetailCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(NewsDetail)
    
    def get_pages_news(self,db: Session,page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        分页查询新闻
        :param db: 数据库会话
        :param page: 当前页码，从1开始
        :param page_size: 每页数量
        :return: 包含总数和新闻列表的字典
        """
        # 计算偏移量
        skip = (page - 1) * page_size
        
        # 查询分页数据（按发布时间倒序）
        news_list = db.query(NewsDetail)\
            .order_by(NewsDetail.published_at.desc())\
            .offset(skip)\
            .limit(page_size)\
            .all()
        
        # 获取总条数
        total = db.query(NewsDetail).count()
        
        return {
            "total": total,
            "news_detail_list": news_list,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,  # 计算总页数
            "status": 200
        }
    
    def get_pages_news_by_category_id(self,db:Session,page: int = 1, page_size: int = 10, category_id: int = None) -> Dict[str, Any]:
        """
        分页查询新闻
        :param db: 数据库会话
        :param page: 当前页码，从1开始
        :param page_size: 每页数量
        :param category_id: 新闻分类ID
        :return: 包含总数和新闻列表的字典
        """
        # 计算偏移量
        skip = (page - 1) * page_size

        # 查询分页数据
        news_list = db.query(NewsDetail)\
            .filter(NewsDetail.category_id == category_id)\
            .order_by(NewsDetail.published_at.desc())\
            .offset(skip)\
            .limit(page_size)\
            .all()
        
        # 获取该分类下的总条数
        total = db.query(NewsDetail).filter(NewsDetail.category_id == category_id).count()

        return {
            "total": total,
            "news_detail_list": news_list,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,  # 获取总页数
            "status": 200
        }
    
    def get_news_detail_by_id(self,db: Session,news_id: int) -> Dict[str, Any]:
        """
        根据ID查询新闻
        :param db: 数据库会话
        :param news_id: 新闻ID
        :return: 新闻详情
        """
        news_detail = db.query(NewsDetail).filter(NewsDetail.id == news_id).first()
        return news_detail


