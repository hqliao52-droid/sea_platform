from utils.logger import get_logger,setup_logging
from models.news_model import News

class NewsOperator:
    """
    插入

    调用示例：
        news_id = NewsOperator.insert_news(news_data)
        if news_id:
            print(f"新闻插入成功，ID: {news_id}")
    """
    # 静态方法装饰器，用于定义不需要访问实例或类的方法。
    @staticmethod
    def insert_news(entry):
        from app.config.mysql_config import SessionLocal
        setup_logging()
        logger = get_logger("NewsOperator - insert_news")
        db = SessionLocal()

        try:
            # 防止News实例化失败
            news = News(
                title=entry.get("title") or " ",  # 如果为 None 或空字符串，用 " "
                url=entry.get("url") or " ",
                source=entry.get("source") or " ",
                content=entry.get("content") or " ",
                authors=entry.get("authors") or " ",
                keywords=entry.get("keywords") or " ",
                category=entry.get("category") or " ",
                ai_summary=entry.get("ai_summary") or " ",
                summary=entry.get("summary") or " ",
                published_at=entry.get("published_at")  # 日期类型保持 None
            )

            # 添加到session
            db.add(news)

            # 提交
            db.commit()

            # 刷新对象（获取自增ID）
            db.refresh(news)

            # 返回ID
            logger.info(f"插入成功，ID:{news.id}")
            return news.id
        
        except Exception as e:
            # 出现异常，事务回滚
            db.rollback()
            logger.error(f"插入失败:{e}")

        finally:
            logger.info("数据库关闭！")
            db.close()
    
    @staticmethod
    def insert_mult_news(entries):
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
        from app.config.mysql_config import SessionLocal

        setup_logging()
        logger = get_logger("NewsOperator - insert_mult_news")
        
        db = SessionLocal()
        inserted_ids = []
        
        try:
            news_list = []
            for entry in entries:
                news = News(
                    title=entry.get("title") or " ",
                    url=entry.get("url") or " ",
                    source=entry.get("source") or " ",
                    content=entry.get("content") or " ",
                    authors=entry.get("authors") or " ",
                    keywords=entry.get("keywords") or " ",
                    category=entry.get("category") or " ",
                    ai_summary=entry.get("ai_summary") or " ",
                    summary=entry.get("summary") or " ",
                    published_at=entry.get("published_at")
                )
                news_list.append(news)
            
            db.add_all(news_list)
            db.commit()
            
            # 获取插入的ID
            for news in news_list:
                db.refresh(news)
                inserted_ids.append(news.id)

            logger.info(f"插入成功，IDS:{inserted_ids} 批量插入成功，共 {len(inserted_ids)} 条")
            return inserted_ids
            
        except Exception as e:
            db.rollback()
            logger.error(f"批量插入失败:{e}")
            return []
        finally:
            logger.info("数据库关闭！")
            db.close()
