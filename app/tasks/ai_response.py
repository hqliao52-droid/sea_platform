from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from app.prompt.agent_prompt import prompt as AgentPrompt
from app.config.llm_config import llm_config
from app.schemas.news.news_analysis import NewsAnalysis

def llm_check_outreach_news(title: str, content: str) -> dict:
        llm_prompt = AgentPrompt.DouBaoSeedLiteSystemPromptPolicJudge()
        # Prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", llm_prompt),

            ("user", "标题：{title}\n内容：{content}")
        ])

        # 组装流水线
        chain = prompt | llm_config.category_llm() | StrOutputParser()

        # 执行
        return chain.invoke({
            "title": title,
            "content": content
        })

def llm_analyze_news(title: str, content: str,tags_description) -> dict:
        parser = JsonOutputParser(pydantic_object=NewsAnalysis)
        llm_prompt = AgentPrompt.DouBaoSeedLiteSystemPromptNewsSummarize()
        prompt = ChatPromptTemplate.from_messages([
            ("system", llm_prompt + "\n{format_instructions}" + "\n{tags_description}"),
            ("user", "标题：{title}\n内容：{content}")
        ])
        chain = prompt | llm_config.summary_llm() | parser
        return chain.invoke({
            "title": title,
            "content": content,
            "format_instructions": parser.get_format_instructions(),
            "tags_description": tags_description

        })
