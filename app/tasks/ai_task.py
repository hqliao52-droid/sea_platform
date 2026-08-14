import time,json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
)

from app.tasks.celery_app import celery_app
from app.config.redis_config import RedisConfig
from app.services.chat_message_service import ChatMessageOperator
from app.services.news_detail_service import NewsDetailOperator
from app.services.chat_session_service import ChatSessionOperator
from app.rag.pipelines.chat_pipeline import ChatRagPipeline
from app.schemas.chat_message.chat_message import ChatMsg
from app.utils.logger import Logger
from app.rag.prompt.agent_prompt import prompt as AgentPrompt
from app.rag.status_node.chat_node import ChatNode
from app.config.llm_config import llm_config


async def session_topic_generator(user_input:str):
    llm = await llm_config.summary_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", AgentPrompt.doubao_service_dialog_topic_generator()),
        ("user", "{query}"),
    ])
    chain =  prompt | llm
    response: AIMessage = chain.invoke({"query": user_input})
    data = message_to_dict(response)
    return data

def message_to_dict(message: AIMessage) -> dict:
    """将 AIMessage 转换为可直接 JSON 序列化的字典"""
    return {
        "content": message.content,
        "additional_kwargs": message.additional_kwargs,
        "response_metadata": message.response_metadata,
        "id": message.id,
        "tool_calls": message.tool_calls,
        "invalid_tool_calls": getattr(message, "invalid_tool_calls", []),
        "usage_metadata": getattr(message, "usage_metadata", None)
    }

@celery_app.task(bind=True, name="ai.run_llm_task")
async def run_llm_task(self,task_id:str,ai_msg_id:str,user_dialog_id,req:dict):
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
    logger = Logger.setup_logger(f"llm_task_celery_{time.strftime('%Y_%m_%d')}")
    
    try:
        status_node.analyzing(task_id)
        logger.info(f"LLM处理开始:{req['query']}")
        refer_data = []
        if req.get("news_ids"):
            for id in req.get("news_ids"):
                news = await news_detail.get_news_detail_by_id(id)
                logger.info(f"用户当前引用的文章{news.title}")
                refer_data.append(news)

        status_node.retrieving(task_id)
        dialog_history = []
        if req.get("user_id") and req.get("session_id"):
            dialog_history = await chat_message_operator.get_dialog_history(req.get("user_id"),req.get("session_id"),user_dialog_id)
        chunks = []
        for chunk in await pipeline.run_stream(req.get("query"),task_id, refer_data, dialog_history):
            await redis_client.append_stream(task_id,chunk)
            chunks.append(chunk)
        
        logger.info(f"LLM处理结束{chunks}")
        full_text = "".join(chunks)
        
        # 结束标识
        status_node.end(task_id)
        await redis_client.client.expire(f"stream:{task_id}", 300)
        chat_message = await chat_message_operator.get_chat_message_by_id(ai_msg_id)

        if chat_message:
            update_data = {
                "status": "done",
                "content": full_text
            }
            await chat_message_operator.update_by_id(ai_msg_id,update_data)
    except Exception as e:
        msg = await chat_message_operator.get_chat_message_by_id(ai_msg_id)
        if msg:
            update_data = {"status":"error"}
            await chat_message_operator.update_by_id(ai_msg_id,update_data)

        logger.error(f"LLM处理失败{str(e)}")
        status_node.error(task_id)


@celery_app.task(bind=True, name="ai.run_llm_task_session_topic")
async def run_llm_task_session_topic(self, session_id:int, query:str):
    """判断当前会话是否为新会话，如果是，则更新会话主题"""
    chat_session_operator = ChatSessionOperator()
    logger = Logger.setup_logger(f"llm_task_celery_{time.strftime('%Y_%m_%d')}")

    try:
        chat_session = await chat_session_operator.get_chat_session_by_id(session_id)
        logger.info(f"会话信息{chat_session}")
        if chat_session.session_topic == "新会话":
            session_topic = await session_topic_generator(query)
            logger.info(f"会话主题生成成功：{session_topic}")
            topic = {"session_topic":session_topic["content"]}
            obj = await chat_session_operator.update_session(session_id,topic)
            logger.info(f"会话主题更新：{obj}")
    
    except Exception as e:
        logger.error(f"会话主题更新失败：{str(e)}")