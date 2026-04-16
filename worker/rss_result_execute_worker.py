import sys,json
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent)) 

from app.config.rabbitMq_config import MQClient
from app.utils.logger import Logger
from app.tasks.ai_task import llm_check_outreach_news,llm_analyze_news
from app.services.news_service import NewsOperator
from app.services.news_detail_service import NewsDetailOperator
from app.models.news_model import News
from app.models.news_details_model import NewsDetail
from app.services.category_service import CategoryOperator
from app.schemas.category.category import categoryBase
from app.utils.fetch_full_text import fetch_full_text
from concurrent.futures import ThreadPoolExecutor

news_detail_operator = NewsDetailOperator()
logger = Logger.setup_logger(Logger.set_file_name("worker"))
# 并发线程池
executor = ThreadPoolExecutor(max_workers=3)

def news_execute(entry, llm_result, llm_json):
    logger.info(f"是否政策：{llm_result}")
    logger.info(f"AI 输出：{llm_json}")

    news = News()
    news_operator = NewsOperator()
    news_detail = NewsDetail()
    obj = None

    # 每次都重新获取最新分类！！！
    category_operator = CategoryOperator()
    categories = category_operator.get_category_is_active()
    tags = [categoryBase(**tag.__dict__) for tag in categories]
    logger.info(f"当前有效分类：{tags}")

    try:
        if entry:
            news.title = entry["title"]
            news.url = entry["url"]
            news.source = entry["source"]
            news.published_at = entry["published_at"]
            news.is_policy = 1 if llm_result == "1" else 0

            # 默认值
            news.category_name = "其他"
            news.category_id = 20
            # 默认 其他
            news_detail.category_id = 20
            news_detail.category_name = "其他"

            industry = (llm_json or {}).get("industry_category", "")

            if industry:
                for tag in tags:
                    if industry in tag.tag_name or industry in tag.example:
                        logger.info(f"匹配成功：{tag}, 匹配对象：{industry}")
                        
                        news.category_id = tag.id
                        news.category_name = tag.tag_name

                        news_detail.category_id = tag.id
                        news_detail.category_name = tag.tag_name
                        # 匹配成功：找到就 break
                        break

            result = news_operator.insert_news(news)

        else:
            return 
    
        if (llm_result == "1" or llm_result == 1) and result["id"]:
            logger.info("需求类数据，详情插入...")
            news_detail.news_id = result["id"]
            news_detail.title = entry["title"]
            
            news_detail.authors = entry.get("authors", "")
            news_detail.content = entry.get("content", "")
            news_detail.url = entry.get("url", "")
            news_detail.keywords = entry.get("keywords", "")
            news_detail.ai_origin_output = llm_json
            news_detail.summary = entry.get("summary", "")
            news_detail.origin_entry = entry
            news_detail.publiced_at = entry.get("published_at", "")
            
            full_context = fetch_full_text(entry["url"])
            news_detail.in_full_page = full_context.get("content") if full_context.get("status") == "success" else None

            obj = news_detail_operator.insert_news_detail(news_detail)

        
        if result["status"] == "success":
            logger.info({
                "status": 200,
                "msg": "插入成功",
                "news_id": result["id"],
                "news_detail":obj if obj else None
            })
        else:
            logger.error({
                "status": 500,
                "msg": "插入失败",
                "error": result["error"]
            })
    
    except Exception as e:
        logger.error({"status":500,"msg":f"插入失败:{str(e)}"})

def handle_message(message):
    try:
        news_operator = NewsOperator()
        status = news_operator.is_news_exits(message["url"], message["published_at"])
        if status["status"] == "exists":
            logger.info("数据已存在，跳过...")
            return
        
        result = llm_check_outreach_news(message["title"],message["content"])
        ai_json = None
        
        if result == "1" or result == 1:
            category_operator = CategoryOperator()
            tags = category_operator.get_category_is_active()

            tags_description = "\n".join(f"{t.tag_name}: {t.example}" for t in tags)

            ai_json = llm_analyze_news(message["title"],message["content"],tags_description)
        
        news_execute(message, result, ai_json)
    except Exception as e:
        logger.error({"status":500,"msg":f"处理失败:{str(e)}"})

def worker():
    mq_client = MQClient()
    print("Worker 启动成功，开始消费消息...")
    
    def handle(ch,method,message):
        future = executor.submit(handle_message, message)
        def callback(fut):
            try:
                # 有异常就抛出去
                fut.result()
                # 消费成功后才ack
                ch.connection.add_callback_threadsafe(lambda: ch.basic_ack(delivery_tag=method.delivery_tag))
            except Exception as e:
                logger.error({"status":500,"msg":f"处理失败:{str(e)}"})
                # 失败后重新入队
                ch.connection.add_callback_threadsafe(lambda: ch.basic_nack(delivery_tag=method.delivery_tag,requeue=True))
        future.add_done_callback(callback)
    # 消息处理
    mq_client.consume(handle)
            

if __name__ == "__main__":
    worker()