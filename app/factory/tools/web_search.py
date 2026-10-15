from __future__ import annotations

import asyncio

from langchain_core.tools import BaseTool, tool

from app.utils.logger import Logger
logger = Logger.setup_logger(Logger.set_file_name("tool_event"))

_BACKENDS = ("tavily", "duckduckgo")

def _make_tavily_tool(api_key: str) -> BaseTool:
    """创建基于 Tavily 的 web_search 工具。"""

    @tool
    async def web_search(query: str, n: int = 5) -> list[dict]:
        """搜索互联网，适合查询最新信息、新闻、价格、文档和时效性事实。

        Args:
            query: A search-ready query that emphasises recency. Include
                terms like "latest", "news", dates, or time ranges.
            n: Number of results to return. Increase for complex topics.
        """
        try:
            from langchain_community.retrievers import TavilySearchAPIRetriever
        except ImportError as exc:
            raise ImportError(
                "langchain-community and tavily-python are required. "
                "Install with: uv add langchain-community tavily-python"
            ) from exc

        logger.debug('Tavily search: "{}" (n={})', query, n)
        retriever = TavilySearchAPIRetriever(
            k=n,
            tavily_api_key=api_key,
        )
        loop = asyncio.get_running_loop()
        docs = await loop.run_in_executor(None, retriever.invoke, query)

        results = [
            {
                "title": doc.metadata.get("title", ""),
                "url": doc.metadata.get("source", ""),
                "content": doc.page_content,
            }
            for doc in docs
        ]
        logger.debug("Tavily search returned {} results", len(results))
        return results

    return web_search


def _make_duckduckgo_tool() -> BaseTool:
    """创建基于 DuckDuckGo 的 web_search 工具。"""

    @tool
    async def web_search(query: str, n: int = 5) -> list[dict]:
        """搜索互联网，适合查询最新信息、新闻、价格、文档和时效性事实。

        Args:
            query: A search-ready query that emphasises recency. Include
                terms like "latest", "news", dates, or time ranges.
            n: Number of results to return. Increase for complex topics.
        """
        try:
            from langchain_community.tools import DuckDuckGoSearchResults
        except ImportError as exc:
            raise ImportError(
                "langchain-community and duckduckgo-search are required. "
                "Install with: uv add langchain-community duckduckgo-search"
            ) from exc

        logger.debug('DuckDuckGo search: "{}" (n={})', query, n)
        ddg = DuckDuckGoSearchResults(num_results=n, output_format="list")
        loop = asyncio.get_running_loop()
        raw = await loop.run_in_executor(None, ddg.invoke, query)

        # raw is list[dict] with keys: snippet, title, link
        results = [
            {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "content": item.get("snippet", ""),
            }
            for item in (raw if isinstance(raw, list) else [])
        ]
        logger.debug("DuckDuckGo search returned {} results", len(results))
        return results

    return web_search


def make_web_search_tool(
    provider: str,
    *,
    api_key: str = "",
) -> BaseTool:
    """按配置创建 web_search LangChain 工具。"""

    if provider == "tavily":
        try:
            if not api_key:
                raise ValueError(
                    "tavily search backend requires app.tools.web_search.tavily_api_key "
                    "or TAVILY_API_KEY to be set."
                )
            return _make_tavily_tool(api_key)
        except Exception as e:
            logger.error("Tavily search failed: {}", e)
            return _make_duckduckgo_tool()

    if provider == "duckduckgo":
        return _make_duckduckgo_tool()

    raise ValueError(
        f"Unknown search backend: {provider!r}. Choose one of: {', '.join(_BACKENDS)}."
    )
