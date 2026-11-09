

from app.tasks.celery_app import celery_app
from app.config.redis_config import RedisConfig
from app.services.chat_message_service import ChatMessageOperator
from app.services.news_detail_service import NewsDetailOperator
from app.rag.pipelines.chat_pipeline import ChatRagPipeline
from app.models.news_details_model import NewsDetail
from app.utils.log import logger
from app.rag.status_node.chat_node import ChatNode



@celery_app.task(bind=True, name="ai.run_llm_task")
async def run_llm_task(self, task_id: str, ai_msg_id: str, user_dialog_id, req: dict):
    """
    1、调用LLM流式
    2、WebSocket 推送（redis）
    3、更新mysql
    """
    chat_message_operator = ChatMessageOperator()
    news_detail = NewsDetailOperator()
    redis_client = RedisConfig()
    pipeline = ChatRagPipeline()
    status_node = ChatNode()

    try:
        await status_node.analyzing(task_id)
        logger.info(f"LLM处理开始:{req['query']}")
        refer_data: list[NewsDetail] = []
        if req.get("news_ids"):
            for id in req.get("news_ids"):
                news = await news_detail.get_news_detail_by_id(id)
                logger.info(f"用户当前引用的文章{news.title}")
                refer_data.append(news)

        await status_node.retrieving(task_id)
        dialog_history = []
        if req.get("user_id") and req.get("session_id"):
            dialog_history = await chat_message_operator.get_dialog_history(
                req.get("user_id"), req.get("session_id"), user_dialog_id
            )
        chunks = []
        for chunk in await pipeline.run_stream(
            req.get("query"), task_id, refer_data, dialog_history
        ):
            await redis_client.append_stream(task_id, chunk)
            chunks.append(chunk)

        logger.info(f"LLM处理结束{chunks}")
        full_text = "".join(chunks)

        # 结束标识
        await status_node.end(task_id)
        await redis_client.client.expire(f"stream:{task_id}", 300)
        chat_message = await chat_message_operator.get_chat_message_by_id(ai_msg_id)

        if chat_message:
            update_data = {"status": "done", "content": full_text}
            await chat_message_operator.update_by_id(ai_msg_id, update_data)
    except Exception as e:
        msg = await chat_message_operator.get_chat_message_by_id(ai_msg_id)
        if msg:
            update_data = {"status": "error"}
            await chat_message_operator.update_by_id(ai_msg_id, update_data)

        logger.error(f"LLM处理失败{str(e)}")
        await status_node.error(task_id)
