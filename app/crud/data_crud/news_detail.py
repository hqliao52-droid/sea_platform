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
        news_list = db.query(self.model)\
            .order_by(self.model.published_at.desc())\
            .offset(skip)\
            .limit(page_size)\
            .all()
        
        # 获取总条数
        total = db.query(self.model).count()
        
        return {
            "total": total,
            "news_detail_list": news_list,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,  # 计算总页数
            "status": 200
        }

