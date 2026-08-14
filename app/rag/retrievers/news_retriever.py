import time

from langchain_core.messages import SystemMessage

from app.utils.logger import Logger
from app.services.news_detail_service import NewsDetailOperator
from app.rag.prompt.agent_prompt import prompt as AgentPrompt


class NewsRetriever:
    def __init__(self):
        self.logger = Logger.setup_logger(f"llm_task_celery_{time.strftime('%Y_%m_%d')}")
        self.news_detail = NewsDetailOperator()
        
    async def retrieve_by_ids(self,ids, push_status=None):
        # 返回对象：[NewsDetail]仅查title和对应的content
        retrieved_article = await self.news_detail.get_news_detail_by_ids(ids)
        if retrieved_article:
            if push_status:
                push_status("reading")
            retrieved_articles = AgentPrompt.build_retrieved_context(retrieved_article)
            return retrieved_articles