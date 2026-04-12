from celery import Celery

from app.config.settings import settings


# 返回 RabbitMQ 连接地址
def _broker_url() -> str:
    # rabbitmq 默认用户/密码 guest:guest
    return f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:5672//"

# 返回 Redis 连接地址
def _redis_backend() -> str:
    return f"redis://{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

# 创建一个Celery实例 参数：应用名称，消息队列地址（RabbitMQ），结果存储地址（Redis）
celery_app = Celery("sea_ai_platform", broker=_broker_url(), backend=_redis_backend())
# 更新Celery配置
celery_app.conf.update(
    task_serializer="json", # 任务参数用 JSON 序列化
    accept_content=["json"], # 只接受 JSON 格式；防止 pickle（有安全风险）
    result_serializer="json", # 结果用 JSON 序列化
    timezone="Asia/Shanghai", # 时区设置为亚洲上海
    enable_utc=False, # 不使用 UTC 时间
)

# 让 Celery 自动发现 tasks 模块下的任务 app/tasks/*.py
# 它会干什么？
"""
Celery 尝试导入 app.tasks 包下的模块，
只有被成功 import 的模块中的 @task 才会注册
"""
celery_app.autodiscover_tasks(["app.tasks"])

