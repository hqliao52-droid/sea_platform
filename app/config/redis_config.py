import redis
from app.config.settings import settings


class RedisConfig:
    def __init__(self):
        if hasattr(self, "initialized"):
            return
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=0,
            decode_responses=True,
        )
        self.initialized = True

    def init_black_list_token(self,token):
        self.client.set(f"blackList:{token}",15*24*3600,"1")
    
    def check_black_list_token(self,token):
        return self.client.get(f"blackList:{token}" is not None)
