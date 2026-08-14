
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

from app.utils.logger import Logger
from app.rag.prompt.agent_prompt import prompt as AgentPrompt
from app.rag.retrievers.news_retriever import NewsRetriever
from app.rag.status_node.chat_node import ChatNode


class ChatPromptBuilder:
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.news_retriever = NewsRetriever()
        self.status_node = ChatNode()

    async def build_messages(self, user_input:str,task_id:str, refer_data: list = None, history_messages: list = None):
        # 1. 获取基础 System Prompt
        base_system_prompt = AgentPrompt.doubao_service_system_prompt()
        self.logger.info(f"构建基础System Prompt:{base_system_prompt[:20]}")

        messages = [SystemMessage(content=base_system_prompt)]
        
        # 2.  构建会话级文章引用状态
        conversation_state = AgentPrompt.build_conversation_state(refer_data)
        self.logger.info(f"构建会话级文章引用状态:{conversation_state[:30]}")

        if conversation_state:
            messages.append(SystemMessage(content=conversation_state))

        refer_data_status = True
        # 3. 构建历史上下文（短期）
        if history_messages and len(history_messages) > 0:
            # 历史对话中用户主动提出的引用文章列表
            for item in history_messages:
                self.logger.info(f"获取用户引用文章列表:{item}")
                # 数据库该字段存储样式：[ids],null,空
                if refer_data_status and item.llm_refer_data_id and item.llm_refer_data_id != "null":
                    # 只找最近用户引用文章
                    refer_data_status = False
                    # 返回对象：[NewsDetail]仅查title和对应的content
                    self.status_node.reading(task_id)
                    retrieved_articles = await self.news_retriever.retrieve_by_ids(item.llm_refer_data_id)
                    self.logger.info(f"构建文章引用状态:{retrieved_articles[:30]}")
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
        return messages