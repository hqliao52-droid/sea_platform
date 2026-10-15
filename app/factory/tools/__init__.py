from __future__ import annotations

import os

from langchain_core.tools import BaseTool

from app.config.settings import settings
from app.factory.tools.report_security import report_security_event
from app.factory.tools.web_search import make_web_search_tool
from app.factory.tools.image_search import image_search_tool


def _mark_safe_read_tool(tool: BaseTool) -> BaseTool:
    """标记内置联网工具为只读工具，供 allow_safe_tools 权限策略识别。"""
    tool.metadata = {
        **(tool.metadata or {}),
        "source": "builtin",
        "side_effect": "read",
    }
    return tool

def create_tool() -> list[BaseTool]:
    tools: list[BaseTool] = []

    tools.append(_mark_safe_read_tool(
            make_web_search_tool(
                provider=settings.WEB_SEARCH_PROVIDER,
                api_key=settings.TAVILY_API_KEY,
            )
        )
    )

    tools.append(
        _mark_safe_read_tool(image_search_tool)
        if settings.ENABLED_IMAGES_SEARCH
        else None
    )

    tools.append(report_security_event)

    return tools

