from app.utils.logger import Logger
from app.models.category import category
from app.crud.data_crud.category import category_curd

class CategoryOperator:
    """
    插入

    调用示例：
        news_id = NewsOperator.insert_news(news_data)
        if news_id:
            print(f"新闻插入成功，ID: {news_id}")
    """
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())

    def insert_category(self, news_detail_data: category) -> int:
        return category_curd.insert(news_detail_data)
    
    def get_category_is_active(self) -> list[category]:
        return category_curd.get_category_is_active()