from app.crud.sea_data_base import BaseCRUD
from app.models.news_model import News
from app.config.mysql_config import db_session

class NewsCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(News)
    
    def get_pages_news(self,page: int, page_size: int):
        db = db_session()
        try:
            # 计算偏移量
            skip = (page - 1) * page_size

            # 查询分页数据
            news_list = db.query(News).filter(News.is_policy == 1).order_by(News.published_at.desc()).offset(skip).limit(page_size).all()

            # 获取总条数
            total = db.query(News).count()

            return {"total": total, "news_list": news_list,"status": 200}
        except Exception as e:
            return {"message": str(e), "status": 500}
        finally:
            db.close()
    
    
    
# 全局单例，整个程序共用一个连接
news_crud = NewsCRUD()