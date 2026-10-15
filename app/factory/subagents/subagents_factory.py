from __future__ import annotations

from typing import Any
from deepagents import AsyncSubAgent, CompiledSubAgent, SubAgent

from app.factory.base_factory import BaseFactory


class SubagentFactory(BaseFactory):
    """Subagent 工厂。"""

    def __init__(self):
        pass

    def create(
        self, **kwargs: Any
    ) -> list[SubAgent | CompiledSubAgent | AsyncSubAgent]:
        """创建 Subagent。"""
        return []
