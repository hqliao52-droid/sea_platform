from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore

# 全局唯一的调度器实例
# 这就是你要的那行代码，单独封装，所有文件共用这一个实例
scheduler = AsyncIOScheduler(
    jobstores={"default": MemoryJobStore()},
    timezone="Asia/Shanghai"  # 时区
)