from pathlib import Path

from pydantic import BaseModel, Field, Literal

from typing import Literal

from langchain.agents.middleware import AgentMiddleware
from langchain.agents.middleware.context_editing import (
    ClearToolUsesEdit,
    ContextEditingMiddleware,
)
from langchain.agents.middleware.file_search import FilesystemFileSearchMiddleware
from langchain.agents.middleware.pii import PIIMiddleware

from app.factory.base_factory import BaseFactory
from app.factory.middlewares.dangling_tool_call_middleware import DanglingToolCallMiddleware
from app.config.settings import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class AppPIIRuleConfig(BaseModel):
    """单条 PII 检测规则配置。"""

    pii_type: str = Field(default="email", description="PII 类型或自定义类型名。")
    strategy: Literal["block", "redact", "mask", "hash"] = Field(
        default="redact", description="PII 命中后的处理策略。"
    )
    detector: str | None = Field(default=None, description="自定义正则检测器。")
    apply_to_input: bool = Field(default=True, description="是否检测用户输入。")
    apply_to_output: bool = Field(default=False, description="是否检测模型输出。")
    apply_to_tool_results: bool = Field(default=False, description="是否检测工具结果。")

class MiddlewareFactory(BaseFactory):
    """Middleware 工厂"""

    @staticmethod
    def _render_runtime_path(path: str) -> str:
        """渲染依赖运行时上下文的路径配置。"""

        if "{workspace_root}" not in path:
            return path
        return path.replace("{workspace_root}", str(BASE_DIR))


    def create(self, ) -> list[AgentMiddleware]:
        middlewares: list[AgentMiddleware] = []

        middlewares.append(DanglingToolCallMiddleware())

        # 清理工具调用上下文中间件 清理工具调用上下文
        if settings.CONTEXT_EDITING_ENABLED:
            middlewares.append(
                ContextEditingMiddleware(
                    edits=[
                        ClearToolUsesEdit(
                            trigger=settings.CONTEXT_EDITING_CLEAR_TOOL_USES_TRIGGER,
                            clear_at_least=settings.CONTEXT_EDITING_CLEAR_TOOL_USES_CLEAR_AT_LEAST,
                            keep=settings.CONTEXT_EDITING_CLEAR_TOOL_USES_KEEP,
                            clear_tool_inputs=settings.CONTEXT_EDITING_CLEAR_TOOL_USES_INPUTS,
                            exclude_tools=settings.CONTEXT_EDITING_CLEAR_TOOL_USES_EXCLUDE_TOOLS,
                            placeholders=settings.CONTEXT_EDITING_CLEAR_TOOL_USES_PLACEHOLDERS
                        )
                    ],
                    token_count_method=settings.CONTEXT_EDITING_TOKEN_COUNT_METHOD
                )
            )

        # 文件搜索中间件 搜索文件
        if settings.FILESYSTEM_FILE_SEARCH_ENABLED:
            middlewares.append(
                FilesystemFileSearchMiddleware(
                    root_path=self._render_runtime_path(settings.FILESYSTEM_FILE_SEARCH_ROOT_PATH),
                    use_ripgrep=settings.FILESYSTEM_FILE_SEARCH_USE_RIPGREP,
                    max_file_size_mb=settings.FILESYSTEM_FILE_SEARCH_MAX_FILE_SIZE_MB
                )
            )

        # PII 中间件 检测 PII
        if settings.PII_ENABLED:
            pii_config = AppPIIRuleConfig()
            for rule in settings.PII_RULES:
                middlewares.append(
                    PIIMiddleware(
                        rule.pii_type,
                        strategy=rule.strategy,
                        detector=rule.detector,
                        apply_to_input=pii_config.apply_to_input,
                        apply_to_output=pii_config.apply_to_output,
                        apply_to_tool_results=pii_config.apply_to_tool_results
                    )
                )

        return middlewares
