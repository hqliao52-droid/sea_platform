import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent)) 

from app.config.rabbitMq_config import MQClient
from app.utils.logger import Logger
from app.tasks.ai_task import llm_check_outreach_news,llm_analyze_news
from app.services.news_service import NewsOperator
from app.models.news_model import News
from app.utils.fetch_full_text import fetch_full_text
import time


def worker():
    mq_client = MQClient()
    logger = Logger.setup_logger(Logger.set_file_name("worker"))
    newsoperator = NewsOperator()
    while(True):
        msg = mq_client.consume()
        # 没消息就休眠1秒
        if not msg: 
            time.sleep(1)
            continue
        
        for message in msg:
            logger.info(message)
            status = newsoperator.is_news_exits(message["url"],message["published_at"])
            if status["status"] == "exits":
                # 已存在，加速循环
                continue
            result = llm_check_outreach_news(message["title"], message["content"])
            message.update({"is_policy":1 if result == "1" else 0})
            if result == "1":
                ai_json = llm_analyze_news(message["title"], message["content"])
                full_context = fetch_full_text(message["url"])
                logger.info("全文信息：",full_context)
                message.update({"ai_json_output":ai_json})
            try:
                news_obj = News(**message)  # 将 dict 转换为 News 对象
                id = newsoperator.insert_news(news_obj)
                if id:  # 检查是否插入成功
                    logger.info(f"成功插入新闻，ID: {id}")
                    # 未来可做qdrant插入
                else:
                    logger.warning(f"插入失败，返回值为空")

            except Exception as e:
                logger.error(f"插入失败：{str(e)}")

if __name__ == "__main__":
    print("Worker 启动成功，开始消费消息...")
    worker()
