from app.utils.logger import Logger
from app.config.mysql_config import SessionLocal
from app.models.news_model import News
from app.crud.data_crud.news import news_crud

class NewsOperator:
    """
    插入

    调用示例：
        news_id = NewsOperator.insert_news(news_data)
        if news_id:
            print(f"新闻插入成功，ID: {news_id}")
    """
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
    

    def get_pages_news(self,page: int, page_size: int) -> list[News]:
        try:
            # 获取分页数据
            return news_crud.get_pages_news(page, page_size)
        except Exception as e:
            self.logger.error(f"查询失败:{e}")
            return {"status":500,"news_list":None,"total":0}


    # 静态方法装饰器，用于定义不需要访问实例或类的方法。
    # @staticmethod
    def insert_news(self, news:News) -> dict:
        db = SessionLocal()

        try:
            # 添加到session
            db.add(news)

            # 提交
            db.commit()

            # 刷新对象（获取自增ID）
            db.refresh(news)

            # 返回ID
            self.logger.info(f"插入成功，ID:{news.id}")
            return {"id":news.id,"status":"success"}
        
        except Exception as e:
            # 出现异常，事务回滚
            db.rollback()
            self.logger.error(f"插入失败:{e}")

        finally:
            self.logger.info("数据库关闭！")
            db.close()
    
    def is_news_exits(self,url:str,published_at) -> bool:
        db = SessionLocal()
        try:
            id = db.query(News.id).filter(News.url == url,News.published_at == published_at).first()
            self.logger.info(f"新闻已存在，URL:{id}")
            return {"id":id,"status":"exits"} if id else {"id":None,"status":"NotExits"}
        except Exception as e:
            self.logger.error(f"查询失败:{e}")
            return {"id":None,"status":"NotExits"}
        finally:
            self.logger.info("数据库关闭！")
            db.close()
    
    # @staticmethod
    def insert_mult_news(self,news_list:list):
        """
        批量插入多条新闻
        
        Args:
            entries (list): 包含多个新闻字典的列表
            
        Returns:
            list: 成功插入的ID列表

        调用示例：
            multiple_news = [news_data, news_data]  # 实际使用时准备多个新闻数据
            ids = NewsOperator.insert_many_news(multiple_news)
            print(f"批量插入成功，IDs: {ids}")
        """
        db = SessionLocal()
        inserted_ids = []
        try:
            news_instances = []
            for news_dict in news_list:
            # 创建模型实例
                news = News(**news_dict)  # 字典解包，相当于 News(title=xxx, content=xxx)
            news_instances.append(news)


            db.add_all(news_instances)
            db.commit()
            
            # 获取插入的ID
            for news in news_instances:
                db.refresh(news)
                inserted_ids.append(news.id)

            self.logger.info(f"插入成功，IDS:{inserted_ids} 批量插入成功，共 {len(inserted_ids)} 条")
            return inserted_ids
            
        except Exception as e:
            db.rollback()
            self.logger.error(f"批量插入失败:{e}")
            return []
        finally:
            self.logger.info("数据库关闭！")
            db.close()
            
service = NewsOperator()