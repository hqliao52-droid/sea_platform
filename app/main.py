from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from app.config.settings import settings
from app.api.news_api import router as news_router
from app.api.rss_api import router as rss_router
from app.tasks.scheduler import scheduler_task
from app.api.news_detail_api import router as news_detail_router
from app.api.catrgory_api import router as category_router
from app.api.user_api import router as user_router

app = FastAPI(title=settings.APP_NAME,docs_url=None)

app.include_router(news_router, prefix="/news", tags=["news"])
app.include_router(news_detail_router, prefix="/news_detail", tags=["news_detail"])
app.include_router(rss_router, prefix="/rss", tags=["rss"])
app.include_router(category_router, prefix="/category", tags=["category"])
app.include_router(user_router, prefix="/user", tags=["user"])

app.include_router(scheduler_task, tags=["定时任务"])

@app.get("/health")
async def health_check():
    # 可以添加更详细的检查，比如数据库连接等
    return {"status": "healthy"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API 文档",
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.10.5/swagger-ui-bundle.js",  # 使用国内 CDN
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.10.5/swagger-ui.css",
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
