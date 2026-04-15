from app.utils.logger import Logger
from app.models.news_details_model import NewsDetail
from app.crud.data_crud.news_detail import news_detail_crud

class NewsDetailOperator:
    """
    插入

    调用示例：
        news_id = NewsOperator.insert_news(news_data)
        if news_id:
            print(f"新闻插入成功，ID: {news_id}")
    """
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())

    def insert_news_detail(self, news_detail_data: NewsDetail) -> int:
        return news_detail_crud.insert(news_detail_data)