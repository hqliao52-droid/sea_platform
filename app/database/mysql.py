# app/database/mysql.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings


# 数据库URL
DATABASE_URL = (
    f"mysql+pymysql://{settings.MYSQL_USER}:"
    f"{settings.MYSQL_PASSWORD}@"
    f"{settings.MYSQL_HOST}:"
    f"{settings.MYSQL_PORT}/"
    f"{settings.MYSQL_DB}"
)

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 开发阶段可以改为True，开启SQL日志
    pool_pre_ping=True, 
    pool_timeout=30, 
    future=True,  # 使用SQLAlchemy 2.0风格
    pool_recycle=3600,
)

# Session 会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ORM模型基类 Base 作用：所有数据库表都必须继承 Base，因为：Base.metadata会收集所有表结构
"""后面 FastAPI 启动时：Base.metadata.create_all(bind=engine)
    SQLAlchemy 就会：
        扫描所有 Base 子类
        找到表结构
        自动创建数据库表

    ORM 的底层机制：SQLAlchemy
    Python类
    ↓
    ORM映射
    ↓
    SQL语句
    ↓
    MySQL执行
    例如：db.query(News).all()
    就会执行：SELECT * FROM news
"""
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
def get_db():
    print("1. 创建会话")
    db = SessionLocal()
    try:
        print("2. 将会话交给调用者")
        yield db
        print("4. 调用者使用完毕，继续执行")
    finally:
        print("5. 关闭会话")
        db.close()