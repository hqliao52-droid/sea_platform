# app/database/mysql.py
from collections.abc import AsyncGenerator
from app.config.settings import settings
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.utils.logger import Logger

logger = Logger.setup_logger(Logger.set_file_date())

# 数据库URL
DATABASE_URL = (
    f"mysql+aiomysql://{settings.MYSQL_USER}:"
    f"{settings.MYSQL_PASSWORD}@"
    f"{settings.MYSQL_HOST}:"
    f"{settings.MYSQL_PORT}/"
    f"{settings.MYSQL_DB}?charset=utf8mb4"
)

# 创建数据库引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=False, # 并发或者网络状态不好时,建议True
    pool_size=10,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
)

# Session 会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# ORM 模型基类 Base
# 所有数据库表模型都必须继承 Base，因为：
#   1. Base.metadata 会自动收集所有继承它的子类定义的表结构
#   2. 通过 Base.metadata.create_all() 可以一键创建所有表
#
# 异步模式下创建表（在应用启动时执行）：
#   async with engine.begin() as conn:
#       await conn.run_sync(Base.metadata.create_all)
#   （run_sync 用于在异步环境中调用同步的 create_all 方法）
#
# ORM 映射流程：
#   Python 类  →  SQLAlchemy ORM  →  SQL 语句  →  数据库执行
#   例如：await session.execute(select(News))   →  SELECT * FROM news
#
# 查询方式（SQLAlchemy 2.0 风格）：
#   使用 select(模型).where(条件) 构建查询，
#   然后 await session.execute(stmt) 执行，
#   通过 scalars() 或 scalar_one_or_none() 获取结果。
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
            # 如果没有异常，在离开上下文时自动提交
            # await session.commit() # async with 自动处理
        except Exception:
            # 发生异常时回滚
            await session.rollback()
            raise
        finally:
            # 会话会在退出 async with 块时自动关闭
            # await session.close()  # 无需显式调用
            pass


async def init_db():
    """在应用启动时调用，创建所有表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("初始化数据库成功")
async def close_db():
    """在应用关闭时调用，关闭所有连接"""
    await engine.dispose()
