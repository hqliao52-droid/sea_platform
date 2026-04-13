from app.crud.sea_data_base import BaseCRUD
from app.models.news_model import News  # 你的News模型路径

class NewsCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(News)

# 全局单例，整个程序共用一个连接
news_crud = NewsCRUD()