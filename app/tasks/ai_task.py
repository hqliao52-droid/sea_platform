import time
from langchain_core.prompts import ChatPromptTemplate
from celery.utils.log import get_task_logger

from app.tasks.celery_app import celery_app
from app.config.redis_config import redis_client
from app.services.chat_message_service import ChatMessageOperator
from app.utils.logger import Logger
from app.prompt.agent_prompt import prompt as AgentPrompt
from app.config.llm_config import llm_config

logger = Logger.setup_logger(f"llm_task_celery_{time.strftime('%Y_%m_%d')}")

def fake_llm_stream(user_input:str):
    "LLM的流式输出"
    llm_normal = llm_config.get_chat_llm(streaming=True)
    prompt_tpl = ChatPromptTemplate.from_messages([
        ("system", AgentPrompt.doubao_service_system_prompt()),
        ("user", "{query}"),
    ])
    chain = prompt_tpl | llm_normal
    for chunk in chain.stream({"query": user_input}):
        if chunk.content:
            yield chunk.content

@celery_app.task(bind=True, name="ai.run_llm_task")
def run_llm_task(self,task_id:str,prompt:str,ai_msg_id:str):
    """
    1、调用LLM流式
    2、SSE推送（redis）
    3、更新mysql
    """
    chat_message_operator = ChatMessageOperator()
    try:
        logger.info(f"LLM处理开始:{prompt}")
        chunks = []
        for chunk in fake_llm_stream(prompt):
            redis_client.append_stream(task_id,chunk)
            chunks.append(chunk)
        
        logger.info(f"LLM处理结束{chunks}")
        full_text = "".join(chunks)
        
        # 结束标识
        redis_client.append_stream(task_id,"\n[[END]]")
        redis_client.client.expire(f"stream:{task_id}", 300)

        chat_message = chat_message_operator.get_chat_message_by_id(ai_msg_id)

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
