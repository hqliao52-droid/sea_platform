from app.crud.sea_data_base import BaseCRUD
from app.models.news_model import News
from sqlalchemy.orm import Session

class NewsCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(News)
    
    async def get_pages_news(self,db:Session,page: int, page_size: int):
        # 计算偏移量
        skip = (page - 1) * page_size

        # 查询分页数据
        try:
            news_list = await db.query(News).filter(News.is_policy == 1).order_by(News.published_at.desc()).offset(skip).limit(page_size).all()

        # 获取总条数
            total = await db.query(News).count()

            return {"total": total, "news_list": news_list,"status": 200}
        except Exception as e:
            return {"status": 500, "message": "服务器错误"}
    
    async def get_news_by_url(self,db:Session,url:str):
        try:
            news = await db.query(News).filter(News.url == url).first()
            return news
        except Exception as e:
            print(f"{str(e)}")
            return None
    async def get_news_by_id(self,db:Session,id:int):
        try:
            news = await db.query(News).filter(News.id == id).first()
            return news
        except Exception as e:
            print(f"{str(e)}")
            return None
    
    