import time,json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

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

def fake_llm_stream(user_input: str, refer_data: list = None):
    """LLM的流式输出"""
    llm_normal = llm_config.get_chat_llm(streaming=True)
    
    # 1. 获取基础 System Prompt
    base_system_prompt = AgentPrompt.doubao_service_system_prompt()
    
    # 2. 处理引用数据
    context_str = None
    if refer_data and len(refer_data) > 0:
        # 使用 enumerate 获取索引和内容
        # 过滤掉空内容，避免无效引用
        valid_refs = [(idx, content) for idx, content in enumerate(refer_data) if content]
        
        if valid_refs:
            context_parts = []
            for idx, content in valid_refs:
                # 建议限制每篇引用的长度，防止 Prompt 过长超出 Token 限制

                context_parts.append(f"参考资料 {idx + 1}:\n{content}\n")
            
            context_str = "\n---\n".join(context_parts)
            
    # 3. 构建最终 Prompt
    # 策略：如果有引用数据，将其拼接到 System Prompt 中，明确告知模型这是参考信息
    if context_str:
        final_system_prompt = f"{base_system_prompt}\n\n用户提供了以下资料：\n{context_str}"
    else:
        final_system_prompt = base_system_prompt

    prompt_tpl = ChatPromptTemplate.from_messages([
        ("system", final_system_prompt),
        ("user", "{query}"),
    ])
    
    chain = prompt_tpl | llm_normal
    
    for chunk in chain.stream({"query": user_input}):
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
    2、SSE推送（redis）
    3、更新mysql
    """
    
    chat_message_operator = ChatMessageOperator()
    chat_session_operator = ChatSessionOperator()
    news_detail = NewsDetailOperator()
    print(f"会话ID{req['session_id']}")
    print(req["news_ids"])
    try:
        logger.info(f"LLM处理开始:{req['query']}")
        refer_data = []
        if req["news_ids"]:
            for id in req["news_ids"]:
                news = news_detail.get_news_detail_by_id(id)
                refer_data.append(news.content)

        chunks = []
        for chunk in fake_llm_stream(req['query'],refer_data):
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
