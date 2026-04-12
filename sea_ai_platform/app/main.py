from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.news_api import router as news_router

app = FastAPI(title=settings.APP_NAME)

app.include_router(news_router, prefix="/news", tags=["news"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
