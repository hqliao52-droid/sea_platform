from langchain_openai import ChatOpenAI

from app.factory.agent.agent_factory import AgentFactory
from app.config.settings import settings

class LLMConfig:
    def __init__(self):
        self.agent_factory = AgentFactory(
            model=settings.LLM_BASE_MODEL_DEEPSEEK,
            temperature=settings.TEMPERATURE,
        )

    def get_model(self, streaming: bool = False) -> ChatOpenAI:
        return self.agent_factory.create(streaming)


llm_config = LLMConfig()
