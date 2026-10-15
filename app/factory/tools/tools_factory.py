from __future__ import annotations

from typing import Any
from langchain_core.tools import BaseTool
from tools import create_tool

from app.factory.base_factory import BaseFactory

class ToolsFactory(BaseFactory):
    def __init__(self, ):
        pass

    def create(self, **kwargs: Any) -> list[BaseTool]:
        tools: list[BaseTool] = create_tool()
        return tools