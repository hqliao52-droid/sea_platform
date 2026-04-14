from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # 回到项目根目录

class Settings(BaseSettings):
    """项目配置（从环境变量/.env 读取）。"""

    '''读取.env文件，utf-8编码，忽略多余变量；   eg: .env中有SERP_API_KEY变量，但代码中没有SERP_API_KEY变量，则忽略SERP_API_KEY变量，如果没有 extra="ignore" 就会报错'''
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore")

    '''MYSQL_HOST：环境变量名  str：类型   localhost：默认值'''
    '''【核心规则】
        环境变量会覆盖默认值
        代码：MYSQL_HOST: str = "localhost"
        .env
            MYSQL_HOST=db_server
        最终：
            settings.MYSQL_HOST == "db_server"
    '''
    APP_NAME: str = "sea_ai_platform"

    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str
    MYSQL_DB: str = "sea_data"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASSWORD: str

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: str | None = None

    '''意思：
        允许为空，等价Optional[str]
        如果.env没有写，那么
            settings.LLM_API_KEY_DeepSeek = None
    '''
    LLM_API_KEY_DouBaoSeedLite: str | None = None
    LLM_BASE_URL_DouBaoSeedLite: str | None = None
    LLM_MODEL_DouBaoSeedLite: str | None = None

    LOG_DIR: str = "logs"


'''settings = Settings() 实例化
    step:
        读取.env文件
        匹配字段
        类型转换
        生成对象
    最终：
        settings = Settings(
            MYSQL_HOST="localhost",
            MYSQL_PORT=3306,
            MYSQL_USER="root",
            MYSQL_PASSWORD="CDZSMySQL20250829",
            MYSQL_DB="sea_data",
            REDIS_HOST="redis",
            REDIS_PORT=6379,
            RABBITMQ_HOST="rabbitmq",
            LLM_API_KEY_DeepSeek="4b23f71f-963c-4d9e-b2e3-4971a1b47d8b",
            ...
        )

'''
settings = Settings()

'''【使用方式】
    其他文件只需要：
        from data.settings import settings
'''

