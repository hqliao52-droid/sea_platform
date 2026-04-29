from langchain_openai import ChatOpenAI
from app.config.settings import settings

class LLMConfig:
    def __init__(self):
        # 一次性初始化豆包（兼容 OpenAI 格式）
        pass
    def get_chat_llm(self,streaming:bool = True):
        return  ChatOpenAI(
            model=settings.LLM_MODEL_DouBaoSeedLite,
            api_key=settings.LLM_API_KEY_DouBaoSeedLite,
            base_url=settings.LLM_BASE_URL_DouBaoSeedLite,
            temperature=0.7,
            streaming=streaming
        )


    def category_llm(self):
        return ChatOpenAI(
            model=settings.LLM_MODEL_DouBaoSeedLite,
            api_key=settings.LLM_API_KEY_DouBaoSeedLite,
            base_url=settings.LLM_BASE_URL_DouBaoSeedLite,
            temperature=0.1,
        )

    def summary_llm(self):
        return ChatOpenAI(
            model=settings.LLM_MODEL_DouBaoSeedLite,
            api_key=settings.LLM_API_KEY_DouBaoSeedLite,
            base_url=settings.LLM_BASE_URL_DouBaoSeedLite,
            temperature=0.7,
        )

    
llm_config = LLMConfig()