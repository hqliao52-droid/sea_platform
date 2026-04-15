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

category_operator = CategoryOperator()
news_operator = NewsOperator()
tags = category_operator.get_category_is_active()
news_detail_operator = NewsDetailOperator()
logger = Logger.setup_logger(Logger.set_file_name("worker"))


def news_execute(entry,llm_result,llm_json):
    news = News()
    news_detail = NewsDetail()
    # news主表ID
    id = None
    try:
        if entry:
            news.title = entry["title"]
            news.url = entry["url"]
            news.source = entry["source"]
            news.published_at = entry["published_at"]
            id = news_operator.insert_news(news)
    
        if llm_result == "1":
            news_detail.news_id = id
            news_detail.title = entry["title"]
            for tag in tags:
                if llm_json["industry_category"] in tag.tag_name or llm_json["industry_category"] in tag.example:
                    news_detail.category_id = tag.id
                    news_detail.category_name = tag.tag_name
                else:
                    news_detail.category_id = 20
                    news_detail.category_name = "其他"
            
            news_detail.authors = entry["authors"] or ""
            news_detail.content = entry["content"] or ""
            news_detail.url = entry["url"] or ""
            news_detail.keywords = entry["keywords"] or ""
            news_detail.ai_origin_output = llm_json
            news_detail.summary = entry["summary"] or ""
            news_detail.origin_entry = entry
            news_detail.publiced_at = entry["published_at"]
            full_context = fetch_full_text(entry["url"])
            news_detail.in_full_page = full_context["content"] if full_context["status"] == "success" else None

            obj = news_detail_operator.insert_news_detail(news_detail)
    
        logger.info({"status":200,"msg":"插入成功","news_id":id,"news_detail":obj})
    except Exception as e:
        logger.error({"status":500,"msg":f"插入失败,{str(e)}"})


def worker():
    mq_client = MQClient()
    while(True):
        msg = mq_client.consume()
        # 没消息就休眠1秒
        if not msg: 
            time.sleep(1)
            continue
        
        for message in msg:
            logger.info(message)
            status = news_operator.is_news_exits(message["url"],message["published_at"])
            if status["status"] == "exits":
                # 已存在，加速循环
                continue
            result = llm_check_outreach_news(message["title"], message["content"])
            message.update({"is_policy":1 if result == "1" else 0})
            ai_json = None
            if result == "1":
                tags_description = "行业类别：\n"
                for tag in tags:
                    tags_description += tag.tag_name + ": " + tag.example + " \n"
                ai_json = llm_analyze_news(message["title"], message["content"],tags_description)
            
            news_execute(message,result,ai_json)
            

if __name__ == "__main__":
    print("Worker 启动成功，开始消费消息...")
    worker()
