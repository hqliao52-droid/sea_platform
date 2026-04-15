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
from app.utils.fetch_full_text import fetch_full_text
import time

# 不要全局实例化！！！
# category_operator = CategoryOperator()
# news_operator = NewsOperator()
# tags = category_operator.get_category_is_active()

news_detail_operator = NewsDetailOperator()
logger = Logger.setup_logger(Logger.set_file_name("worker"))


def news_execute(entry, llm_result, llm_json):
    news = News()
    news_operator = NewsOperator()
    news_detail = NewsDetail()
    news_id = None
    obj = None

    # 每次都重新获取最新分类！！！
    category_operator = CategoryOperator()
    tags = category_operator.get_category_is_active()

    try:
        if entry:
            news.title = entry["title"]
            news.url = entry["url"]
            news.source = entry["source"]
            news.published_at = entry["published_at"]
            news.is_policy = 1 if llm_result == "1" else 0
            news_id = news_operator.insert_news(news)
    
        if llm_result == "1" and news_id:
            news_detail.news_id = news_id
            news_detail.title = entry["title"]
            
            # 默认 其他
            news_detail.category_id = 20
            news_detail.category_name = "其他"

            # 正确匹配：找到就 break
            for tag in tags:
                industry = llm_json.get("industry_category", "")
                if industry in tag.tag_name or industry in tag.example:
                    logger.info(f"匹配成功：{tag}, 匹配对象：{industry}")
                    news_detail.category_id = tag.id
                    news_detail.category_name = tag.tag_name
                    break
            
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
    
        logger.info({"status":200,"msg":"插入成功","news_id":news_id,"news_detail":obj.id if obj else None})
    except Exception as e:
        logger.error({"status":500,"msg":f"插入失败:{str(e)}"})


def worker():
    mq_client = MQClient()
    print("Worker 启动成功，开始消费消息...")
    
    # 每次循环都新建 service，不共用、不全局
    news_operator = NewsOperator()

    while True:
        msg = mq_client.consume()
        if not msg: 
            time.sleep(1)
            continue
        
        for message in msg:
            logger.info(message)
            try:
                # 每次查询都新建连接
                status = news_operator.is_news_exits(message["url"], message["published_at"])
                if status["status"] == "exists":
                    continue

                # AI 判断
                result = llm_check_outreach_news(message["title"], message["content"])
                ai_json = None

                if result == "1":
                    # 每次都获取最新分类！
                    category_operator = CategoryOperator()
                    tags = category_operator.get_category_is_active()
                    
                    tags_description = "行业类别：\n"
                    for tag in tags:
                        tags_description += f"{tag.tag_name}: {tag.example}\n"
                    
                    ai_json = llm_analyze_news(message["title"], message["content"], tags_description)
            
                news_execute(message, result, ai_json)
            except Exception as e:
                logger.error(f"单条消息处理失败：{e}")
            

if __name__ == "__main__":
    worker()