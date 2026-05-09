import time,json
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder,ToolMessage
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
) 

from app.tasks.celery_app import celery_app
from app.config.redis_config import redis_client
from app.services.chat_message_service import ChatMessageOperator
from app.services.news_detail_service import NewsDetailOperator
from app.services.chat_session_service import ChatSessionOperator
from app.schemas.chat_message.chat_message import ChatMsg
from app.utils.logger import Logger
from app.prompt.agent_prompt import prompt as AgentPrompt
from app.config.llm_config import llm_config

logger = Logger.setup_logger(f"llm_task_celery_{time.strftime('%Y_%m_%d')}")

def fake_llm_stream(user_input: str, refer_data: list = None, history_messages: list = None):
    """LLM的流式输出"""
    llm_normal = llm_config.get_chat_llm(streaming=True)
    
    # 1. 获取基础 System Prompt
    base_system_prompt = AgentPrompt.doubao_service_system_prompt()
    logger.info(f"构建基础System Prompt:{base_system_prompt[:20]}")

    messages = [SystemMessage(content=base_system_prompt)]
    
    # 2.  构建会话级文章引用状态
    conversation_state = AgentPrompt.build_conversation_state(refer_data)
    logger.info(f"构建会话级文章引用状态:{conversation_state[:30]}")

    if conversation_state:
        messages.append(SystemMessage(content=conversation_state))

    refer_data_status = True
    # 3. 构建历史上下文
    if history_messages and len(history_messages) > 0:
        # 历史对话中用户主动提出的引用文章列表
        news_detail = NewsDetailOperator()
        for item in history_messages:
            logger.info(f"获取用户引用文章列表:{item}")
            # 数据库该字段存储样式：[ids],null,空
            if refer_data_status and item.llm_refer_data_id and item.llm_refer_data_id != "null":
                # 只找最近用户引用文章
                refer_data_status = False
                # 返回对象：[NewsDetail]仅查title和对应的content
                retrieved_article = news_detail.get_news_detail_by_ids(item.llm_refer_data_id)
                if retrieved_article:
                    retrieved_articles = AgentPrompt.build_retrieved_context(retrieved_article)
                    logger.info(f"构建文章引用状态:{retrieved_articles[:30]}")
                    messages.append(SystemMessage(content=retrieved_articles))

        # 由于查询出来对话历史是最近几条，为倒序，需要按照ID重新排序
        history_messages.sort(key=lambda x: x.id)
        for item in history_messages:
            if item.message_type == 1:
                messages.append(HumanMessage(content=item.content))
            elif item.message_type == 2:
                messages.append(AIMessage(content=item.content))
            # elif item.message_type == 4:
            #     messages.append(ToolMessage(content=item.content))
    # 当前用户对话
    messages.append(HumanMessage(content=user_input))
    
    for chunk in llm_normal.stream(messages):
        if chunk.content:
            yield chunk.content

def session_topic_generator(user_input:str):
    llm = llm_config.summary_llm()
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
def run_llm_task(self,task_id:str,ai_msg_id:str,req:dict):
    """
    1、调用LLM流式
    2、WebSocket 推送（redis）
    3、更新mysql
    """
    
    chat_message_operator = ChatMessageOperator()
    chat_session_operator = ChatSessionOperator()
    news_detail = NewsDetailOperator()
    try:
        logger.info(f"LLM处理开始:{req['query']}")
        refer_data = []
        if req.get("news_ids"):
            for id in req.get("news_ids"):
                news = news_detail.get_news_detail_by_id(id)
                logger.info(f"用户当前引用的文章{news.title}")
                refer_data.append(news.content)

        dialog_history = []
        if req.get("user_id") and req.get("session_id"):
            dialog_history = chat_message_operator.get_dialog_history(req.get("user_id"),req.get("session_id"),ai_msg_id)

        chunks = []
        for chunk in fake_llm_stream(req.get("query"), refer_data, dialog_history):
            redis_client.append_stream(task_id,chunk)
            chunks.append(chunk)
        
        logger.info(f"LLM处理结束{chunks}")
        full_text = "".join(chunks)
        
        # 结束标识
        redis_client.append_stream(task_id,"\n[[END]]")
        redis_client.client.expire(f"stream:{task_id}", 300)

        chat_message = chat_message_operator.get_chat_message_by_id(ai_msg_id)

        chat_session = chat_session_operator.get_chat_session_by_id(req["session_id"])
        logger.info(f"会话信息{chat_session}")
        if chat_session.session_topic == "新会话":
            session_topic = session_topic_generator(req["query"])
            logger.info(f"会话主题生成成功：{session_topic}")
            topic = {"session_topic":session_topic["content"]}
            obj = chat_session_operator.update_session(req["session_id"],topic)
            logger.info(f"会话主题更新：{obj}")

        if chat_message:
            update_data = {
                "status": "done",
                "content": full_text
            }
            updated = chat_message_operator.update_by_id(ai_msg_id,update_data)
            if updated:
                return "success"
    except Exception as e:
        msg = chat_message_operator.get_chat_message_by_id(ai_msg_id)
        if msg:
            update_data = {"status":"error"}
            updated = chat_message_operator.update_by_id(ai_msg_id,update_data)

        logger.error(f"LLM处理失败{str(e)}")
        redis_client.append_stream(task_id,"\n[[ERROR]]")
        raise e
