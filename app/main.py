import asyncio
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from contextlib import asynccontextmanager

from app.config.settings import settings
from app.config.file_config import file_config
from app.config.pg_config import init_db, close_db
from app.config.langgraph_postgres import test_langgraph_postgres
from app.config.langgraph_postgres import DATABASE_URL
from app.config.redis_config import redis_client
from app.middlewares.request_log_middleware import RequestLogMiddleware
from app.utils.log import logger
from app.utils.result_response import Result, ResultCode
from app.api.news_api import router as news_router
from app.api.rss_api import router as rss_router
from app.api.news_detail_api import router as news_detail_router
from app.api.catrgory_api import router as category_router
from app.api.user_api import router as user_router
from app.api.file_api import router as file_router
from app.api.chat_session_api import chat_session_router
from app.api.chat_message_api import chat_message_router
from app.api.user_config_api import router as user_config_router
from app.api.email_api import router as email_router
from app.api.llm_api import router as llm_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    scheduler = None
    if settings.RSS_SCHEDULER_ENABLED:
        try:
            logger.info("正在初始化定时任务...")
            from app.core.scheduler import scheduler
            from app.tasks.crwal_task import spider_rss
            
            if not scheduler.running:
                scheduler.start()
            asyncio.create_task(spider_rss())
            scheduler.add_job(
                spider_rss, 
                'interval', 
                minutes=30, 
                id="sync_rss_sources_job",
                replace_existing=True
            )
            logger.info("定时任务已启动")
        except Exception as e:
            logger.error(f"定时任务启动失败：{e}")
    try:
        async with AsyncPostgresSaver.from_conn_string(
            DATABASE_URL
        ) as checkpointer:
            await checkpointer.setup()
            app.state.checkpointer = checkpointer
            yield
    finally:
        logger.info("应用正在关闭，开始清理资源...")
        if settings.RSS_SCHEDULER_ENABLED:
            from app.core.scheduler import scheduler
            if scheduler.running:
                scheduler.shutdown(wait=False)
                logger.info("调度器已安全关闭！")
        try:
            await close_db()
        finally:
            await redis_client.close()
        logger.info("资源清理完毕。")

    


app = FastAPI(
    title=settings.APP_NAME, 
    docs_url=None, 
    redoc_url=None,
    # openapi_url=None,
    lifespan=lifespan
)

app.include_router(news_router, prefix="/news", tags=["news"])
app.include_router(news_detail_router, prefix="/news_detail", tags=["news_detail"])
app.include_router(rss_router, prefix="/rss", tags=["rss"])
app.include_router(category_router, prefix="/category", tags=["category"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(file_router, prefix="/file", tags=["文件接口"])
app.include_router(chat_session_router, prefix="/session", tags=["会话接口"])
app.include_router(chat_message_router, prefix="/chatMessage", tags=["用户消息接口"])
app.include_router(user_config_router, prefix="/userConfig", tags=["用户配置接口"])
app.include_router(email_router, prefix="/email", tags=["邮件接口"])
app.include_router(llm_router, prefix="/llm", tags=["AI对话"])


app.add_middleware(RequestLogMiddleware)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """兜底异常处理：任何未处理异常都写一条 ERROR 日志，并返回统一响应结构。

    完整堆栈由 RequestLogMiddleware 打印（带 request_id），这里只补一行摘要，
    避免同一个异常在控制台刷两遍 traceback。
    """
    logger.error(
        "[{}] 系统异常：500 | {} {} | {}: {}",
        getattr(request.state, "request_id", "-"),
        request.method,
        request.url.path,
        type(exc).__name__,
        exc,
    )
    return JSONResponse(
        status_code=500,
        content=Result.error(ResultCode.SYSTEM_ERROR).model_dump(),
    )



@app.get("/health")
async def health_check():
    # 可以添加更详细的检查，比如数据库连接等
    _loging = await test_langgraph_postgres()
    return {
        "status": "healthy",
        "langgraph_postgres": _loging
        }

# FastAPI 默认是不能访问本地文件的，需要加上静态文件访问
# git 不跟踪空目录，新克隆/新部署的环境里 attach 可能不存在，StaticFiles 会直接抛
# RuntimeError: Directory 'attach' does not exist，导致进程启动即崩溃，所以这里先建好目录
for _dir in (
    file_config.ATTACH_DIR,
    file_config.IMAGE_DIR,
    file_config.DOC_DIR,
    file_config.VIDEO_DIR,
    file_config.AUDIO_DIR,
    file_config.OTHER_DIR,
    file_config.APP_DIR,
    file_config.BASE_DIR / "static",
):
    Path(_dir).mkdir(parents=True, exist_ok=True)

app.mount("/attach", StaticFiles(directory=str(file_config.ATTACH_DIR)), name="attach")
app.mount("/static", StaticFiles(directory=str(file_config.BASE_DIR / "static")), name="static")

@app.get("/docs-cn", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API 文档",
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.10.5/swagger-ui-bundle.js",  # 使用国内 CDN
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.10.5/swagger-ui.css",
    )

@app.get("/docs-zh", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API 文档",
        # 改成指向你本机的静态文件路径
        swagger_js_url="/static/swagger-ui-bundle.js", 
        swagger_css_url="/static/swagger-ui.css",
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
