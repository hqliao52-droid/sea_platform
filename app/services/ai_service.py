from langchain_core.prompts import ChatPromptTemplate
from app.config.llm_config import llm_config
from app.prompt.agent_prompt import prompt as AgentPrompt
from app.utils.logger import Logger


class AIService:
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_logger_file_llm())
        self.llm_normal = llm_config.get_chat_llm(streaming=True)

    async def DouBaoSeedLite(self,query:str):

        prompt = ChatPromptTemplate.from_messages([
            ("system", AgentPrompt.doubao_service_system_prompt()),
            ("user", "{query}")
        ])
        chain = prompt | self.llm_normal
        async for chunk in chain.astream({"query": query}):
            if chunk.content:
                yield chunk.content

ai_service = AIService()