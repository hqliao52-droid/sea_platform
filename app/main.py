from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.news_api import router as news_router
from app.api.rss_api import router as rss_router

app = FastAPI(title=settings.APP_NAME)

app.include_router(news_router, prefix="/news", tags=["news"])
app.include_router(rss_router, prefix="/rss", tags=["rss"])

@app.get("/health")
async def health_check():
    # 可以添加更详细的检查，比如数据库连接等
    return {"status": "healthy"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
