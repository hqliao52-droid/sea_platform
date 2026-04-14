from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from app.prompt.agent_prompt import prompt as AgentPrompt
from app.config.llm_config import llm_config
from app.schemas.news.news_analysis import NewsAnalysis

def llm_check_outreach_news(title: str, content: str) -> dict:
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

def llm_analyze_news(title: str, content: str) -> dict:
        parser = JsonOutputParser(pydantic_object=NewsAnalysis)
        prompt = ChatPromptTemplate.from_messages([
            ("system", AgentPrompt.DouBaoSeedLiteSystemPromptNewsSummarize()),

            ("user", f"标题：{title}\n内容：{content}")
        ])
        chain = prompt | llm_config.summary_llm() | parser
        return chain.invoke({
            "title": title,
            "content": content,
            "format_instructions": parser.get_format_instructions()
        })

def _llm_analyze_news(title: str, content: str) -> dict:
    # 使用结构化输出（需要模型支持 function calling）
    llm = llm_config.summary_llm()
    structured_llm = llm.with_structured_output(NewsAnalysis)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", AgentPrompt.DouBaoSeedLiteSystemPromptNewsSummarize()),
        ("user", "标题：{title}\n内容：{content}")
    ])
    
    chain = prompt | structured_llm
    result = chain.invoke({"title": title, "content": content})
    
    # 如果 result 是 Pydantic 对象，转为 dict
    return result.dict() if hasattr(result, 'dict') else result