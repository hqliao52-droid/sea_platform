import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent)) 

from app.config.rabbitMq_config import MQClient
from app.utils.logger import Logger
from app.tasks.ai_task import llm_check_outreach_news
from app.services.news_service import NewsOperator
import time


def worker():
    mq_client = MQClient()
    logger = Logger.setup_logger(Logger.set_file_name(worker))
    while(True):
        msg = mq_client.consume()
        # 没消息就休眠1秒
        if not msg: 
            time.sleep(1)
            continue
        
        for message in msg:
            logger.info(message)
            result = llm_check_outreach_news(message["title"], message["content"])
            message.update({"is_policy":1 if result == "1" else 0})
        
        try:
            newsoperator = NewsOperator()
            ids = newsoperator.insert_mult_news(msg)
            logger.info(f"成功插入 {len(ids)} 条news")

        except Exception as e:
            logger.error(f"插入失败：{str(e)}")

if __name__ == "__main__":
    print("Worker 启动成功，开始消费消息...")
    worker()
