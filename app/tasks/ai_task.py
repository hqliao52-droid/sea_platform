from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.prompt.agent_prompt import prompt as AgentPrompt
from app.config.llm_config import llm_config

def llm_check_outreach_news(title: str, content: str) -> str:
        # Prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", AgentPrompt.DouBaoSeedLiteSystemPromptPolicJudge()),

            ("user", f"标题：{title}\n内容：{content}")
        ])

        # 组装流水线
        chain = prompt | llm_config.category_llm() | StrOutputParser()

        # 执行
        return chain.invoke({
            "title": title,
            "content": content
        })