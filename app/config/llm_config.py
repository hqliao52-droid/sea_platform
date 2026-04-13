from langchain_openai import ChatOpenAI

class LLMConfig:
    def __init__(self):
        # 一次性初始化豆包（兼容 OpenAI 格式）
        self.doubao = ChatOpenAI(
            model="ep-20260410155952-vqgg4",
            api_key="4b23f71f-963c-4d9e-b2e3-4971a1b47d8b",
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            temperature=0.1,
        )

    def category_llm(self):
        return self.doubao
    
llm_config = LLMConfig()