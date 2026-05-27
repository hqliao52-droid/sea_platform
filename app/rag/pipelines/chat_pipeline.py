import time

from app.utils.logger import Logger
from app.rag.prompt.builders.chat_prompt_builder import ChatPromptBuilder
from app.rag.status_node.chat_node import ChatNode
from app.config.llm_config import llm_config


class ChatRagPipeline:
    def __init__(self):
        self.logger = Logger.setup_logger(f"llm_task_celery_{time.strftime('%Y_%m_%d')}")
        self.prompt_builder = ChatPromptBuilder()
        self.status_node = ChatNode()
     
    def run_stream(self,user_input: str,task_id:str, refer_data: list = None, history_messages: list = None):
        """LLM的流式输出
        分层上下文架构：
            短期上下文（Recent Messages） N轮
            长期记忆（Conversation Memory Summary） N轮前的记忆
            用户画像（User Profile） 
            当前检索内容（RAG Retrieval）
            工具定义（Tools Schema）
            运行状态（Workflow State）
        """

        llm_normal = llm_config.get_chat_llm(streaming=True)
        
        messages = self.prompt_builder.build_messages(user_input,task_id,history_messages,refer_data)

        self.logger.info("=" * 80)
        self.logger.info("最终发送给 LLM 的 messages：")
        for i, msg in enumerate(messages, start=1):
            role = msg.__class__.__name__
            content = msg.content if msg.content else ""

            # 防止日志过长，只打印前 500 个字符
            preview = content[:500]

            self.logger.info(f"[{i}] {role}")
            self.logger.info(preview)
            self.logger.info("-" * 80)

        self.logger.info("=" * 80)
        self.status_node.generating(task_id)
        for chunk in llm_normal.stream(messages):
            if chunk.content:
                yield chunk.content