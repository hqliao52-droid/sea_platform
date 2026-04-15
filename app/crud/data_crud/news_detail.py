from app.crud.sea_data_base import BaseCRUD
from app.models.news_details_model import NewsDetail  # 你的News模型路径

class NewsDetailCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(NewsDetail)

# 全局单例，整个程序共用一个连接
news_detail_crud = NewsDetailCRUD()