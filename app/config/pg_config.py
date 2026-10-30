# app/database/postgres.py
from collections.abc import AsyncGenerator
from app.config.settings import settings
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.utils.log import logger

# 数据库URL
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.PG_USER}:"
    f"{settings.PG_PASSWORD}@"
    f"{settings.PG_HOST}:"
    f"{settings.PG_PORT}/"
    f"{settings.PG_DB}"
)

# 连接参数
CONNECT_ARGS = {
    "server_settings": {
        "search_path": settings.PG_SCHEMA,
        "application_name": f"{settings.APP_NAME}-{settings.SERVER_ENV}",
        "statement_timeout": "60000",
        "idle_in_transaction_session_timeout": "60000",
    }
}

# 创建数据库引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,      # PG 长连接易被中间件断开，建议开启
    pool_size=10,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    connect_args=CONNECT_ARGS,
)

# Session 会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


# FastAPI依赖
"""
    生成器函数(yield)
    假设其他文件使用到了get_db
    那么实际的工作流程：
        # 使用方式：
            db_gen = get_db()           # 获取生成器
            db = next(db_gen)           # 执行到 yield，获取db
            # 使用db进行数据库操作...
            try:
                next(db_gen)            # 尝试继续执行（触发finally）
            except StopIteration:
                pass                    # 生成器正常结束
"""
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            pass


async def init_db():
    """在应用启动时调用，创建所有表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("初始化数据库成功")
    
async def close_db():
    """在应用关闭时调用，关闭所有连接"""
    await engine.dispose()
