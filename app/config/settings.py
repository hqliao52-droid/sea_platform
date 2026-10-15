from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import ClassVar

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # 回到项目根目录

class Settings(BaseSettings):
    # 项目配置（从环境变量/.env 读取）。
    # 读取.env文件，utf-8编码，忽略多余变量；   
    # eg: 
    #     .env中有SERP_API_KEY变量，但代码中没有SERP_API_KEY变量，则忽略SERP_API_KEY变量，如果没有 extra="ignore" 就会报错
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    APP_NAME: str = "sea_ai_platform"
    SERVER_ENV: str = "test"
    DEBUG: bool = True

    # SQL_ENGINE: 环境变量名  str：类型   localhost：默认值
    # 【核心规则】
    #     环境变量会覆盖默认值
    #     代码：SQL_ENGINE: str = "localhost"
    #     .env
    #         SQL_ENGINE=db_server
    #     最终：
    #         settings.SQL_ENGINE == "db_server"
    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "postgres"
    PG_DB: str = "postgres"
    PG_SCHEMA: str = "public"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_NAME: str = "sea_ai_platform"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASSWORD: str

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: str | None = None

    #  ==================
    #  通用 agent 配置
    #  ==================
    # DeepSeek
    LLM_BASE_URL_DEEPSEEK: str | None = None
    LLM_BASE_MODEL_DEEPSEEK: str | None = None
    LLM_API_KEY_DEEPSEEK: str | None = None
    LLM_DISPLAY_NAME_DEEPSEEK: str | None = None

    # 通用模型配置
    BASE_MODEL: str | None = None
    API_KEY: str | None = None
    BASE_URL: str | None = None
    # LLM 提供商类型 (不同的 Provider 有不同的 API 鉴权方式（Header 不同）、错误重试策略、速率限制逻辑和 Token 计价公式)
    PROVIDER: str | None = None
    # 思考模式
    THINKING_ENABLED: bool | bool = False
    # 是否支持思考模型
    SUPPORTED_THINKING: bool | bool = False
    # 控制思考深度（ low / medium / high ）high 表示模型会进行更长时间的推理链计算。
    REASONING_EFFORT: str | str = "medium"
    # 扩展字典，用于存放额外的元信息（如计费单价、并发限制、负载均衡权重、标签分类等）
    METADATA: dict | dict = {}
    # 温度
    TEMPERATURE: float | float = 0.7
    # 惩罚因子
    ENABLED_PENALTY: bool | bool = False
    FREQUENCY_PENALTY: float | float = 0.5
    PRESENCE_PENALTY: float | float = 0.3

    # agent 工作终端
    BACKEND_DIR: str = str(BASE_DIR / "backend" / "workspace")

    # langfuse
    LANGFUSE_ENABLED: bool | bool = False
    LANGFUSE_SECRET_KEY: str | None = None
    LANGFUSE_PUBLIC_KEY: str | None = None
    LANGFUSE_BASE_URL: str | None = None

    CONTEXT_EDITING_ENABLED: bool | bool = False
    CONTEXT_EDITING_SOURCE: str | None = None
    CONTEXT_EDITING_TOKEN_COUNT_METHOD: str | None = None
    CONTEXT_EDITING_CLEAR_TOOL_USES_TRIGGER: int | int = 1024*256
    CONTEXT_EDITING_CLEAR_TOOL_USES_CLEAR_AT_LEAST: int | int = 0
    CONTEXT_EDITING_CLEAR_TOOL_USES_KEEP: int | int = 3
    CONTEXT_EDITING_CLEAR_TOOL_USES_INPUTS: bool | bool = False
    CONTEXT_EDITING_CLEAR_TOOL_USES_EXCLUDE_TOOLS: list | list = []
    CONTEXT_EDITING_CLEAR_TOOL_USES_PLACEHOLDERS: str | str = "[cleared]"

    FILESYSTEM_FILE_SEARCH_ENABLED: bool | bool = False
    FILESYSTEM_FILE_SEARCH_ROOT_PATH: str | None = None
    FILESYSTEM_FILE_SEARCH_USE_RIPGREP: bool | bool = False
    FILESYSTEM_FILE_SEARCH_MAX_FILE_SIZE_MB: int | int = 10
    FILESYSTEM_FILE_SEARCH_SOURCE: str | None = None

    PII_ENABLED: bool | bool = False
    PII_RULES: list[dict] | list[dict] = []
    PII_SOURCE: str | None = None

    BASE_SYSTEMP_PROMPT: ClassVar[str]="你是一个生产级 Harness Agent。你需要根据用户问题给出清晰、可靠、可执行的回答。"

    BACKEND_NAME: str | None = None

    WEB_SEARCH_PROVIDER: str | None = None
    TAVILY_API_KEY: str | None = None

    ENABLED_IMAGES_SEARCH: bool | bool = False

    # jwt
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    JWT_ALGORITHM: str

    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000

    LOG_DIR: str = "logs"

    """邮箱配置 SMTP配置"""
    SMTP_HOST: str = "smtp.126.com"
    SMTP_PORT: int = 465
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    APK_PATH: str = ""



settings = Settings()
