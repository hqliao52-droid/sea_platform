from celery import Celery

from app.config.settings import settings
from app.utils.logger import Logger

logger = Logger.setup_logger(Logger.set_file_date())


# 返回 RabbitMQ 连接地址
def _broker_url() -> str:
    # rabbitmq 默认用户/密码 guest:guest
    return f"amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASSWORD}@{settings.RABBITMQ_HOST}:5672//"

# 返回 Redis 连接地址
def _redis_backend() -> str:
    if settings.REDIS_PASSWORD:
        return f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
    return f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

# 创建一个Celery实例 参数：应用名称，消息队列地址（RabbitMQ），结果存储地址（Redis）
celery_app = Celery(
    "sea_ai_platform",
    broker=_broker_url(),
    backend=_redis_backend()
)
# 更新Celery配置
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],

    timezone="Asia/Shanghai",
    enable_utc=False,

    # 任务执行行为
    task_acks_late=True,          # worker执行完才ack
    worker_prefetch_multiplier=1, # 防止抢占过多任务

    # 结果过期时间
    result_expires=3600,
)

import app.tasks.ai_task
# 让 Celery 自动发现 tasks 模块下的任务 app/tasks/*.py
# 它会干什么？
"""
Celery 尝试导入 app.tasks 包下的模块，
只有被成功 import 的模块中的 @task 才会注册
"""
# celery_app.autodiscover_tasks(["app.tasks"])

