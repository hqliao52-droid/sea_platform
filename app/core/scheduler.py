from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore

# 全局唯一的调度器实例
scheduler = AsyncIOScheduler(
    jobstores={"default": MemoryJobStore()},
    timezone="Asia/Shanghai"  # 时区
)