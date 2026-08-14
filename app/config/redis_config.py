import redis
from jose import jwt, JWTError
from typing import Any
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

    # access_token 处理
    async def init_black_list_token(self,token):
        await self.client.set(f"blackList:{token}","1",15*24*3600)
    
    async def check_black_list_token(self,token):
        result = await self.client.get(f"blackList:{token}")
        return result is not None
    

    # 流式处理
    async def append_stream(self,task_id:str,chunk:str):
        """追加流式内容"""
        key = f"stream:{task_id}"
        await self.client.append(key,chunk)

    async def get_stream(self,task_id:str):
        """获取流式内容"""
        key = f"stream:{task_id}"
        return await self.client.get(key)
    
    async def add_black_list_token(self, token: str):
        """
        将 JWT Token 加入 Redis 黑名单

        原理：
        1. 解析 JWT，读取其中的 exp（过期时间）
        2. 计算 token 剩余有效秒数
        3. 将 token 存入 Redis，并设置 TTL
        4. 当 token 自然过期后，Redis 自动删除该记录

        Redis Key:
            blackList:<token>

        Redis Value:
            "1"

        为什么这样做？
        - JWT 本身是无状态的
        - 一旦签发，默认无法主动失效
        - Redis 黑名单可以让指定 token 立即失效
        """

        try:
            # 解码 JWT（不校验 exp 是否过期，只读取 exp 字段）
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_exp": False},
            )

            # 获取 JWT 中的过期时间（Unix 时间戳，单位秒）
            exp = payload.get("exp")

            # 如果 token 中没有 exp 字段，则使用默认 15 天
            if not exp:
                ttl = 15 * 24 * 3600
            else:
                # 当前时间戳
                import time
                now = int(time.time())

                # 计算剩余有效时间
                ttl = exp - now

                # 如果 token 已过期，则至少保留 1 秒
                if ttl <= 0:
                    ttl = 1

        except JWTError:
            # 如果 token 解析失败，使用默认 15 天
            ttl = 15 * 24 * 3600

        # Redis 中保存：
        # key   = blackList:<token>
        # value = "1"
        # ex    = ttl（秒）
        await self.client.set(
            f"blackList:{token}",
            "1",
            ex=ttl
        )
    async def delete_stream(self,task_id:str):
        """删除流式内容"""
        key = f"stream:{task_id}"
        await self.client.delete(key)

    # 通用方法处理
    async def set_key(self,key_id: str, value: Any, ttl: int = None) -> bool:
        """ 设置键值对

        Args：
            key_id: 键
            value: 值
            ttl: 过期时间（秒），默认 None
        Returns：
            bool: 设置成功返回 True，否则返回 False 
        """
        return await self.client.set(key_id, value, ex=ttl) is True
    
    async def get_key(self,key_id: str) -> Any:
        """ 获取键值对

        Args：
            key_id: 键
        Returns：
            Any: 键对应的值
        """
        return await self.client.get(key_id)
    
    async def delete_key(self,key_id: str) -> bool:
        """ 删除键值对

        Args：
            key_id: 键
        Returns：
            bool: 删除成功返回 True，否则返回 False
        """
        return bool(await self.client.delete(key_id))
    
    async def key_exists(self,key_id: str) -> bool:
        """ 判断键是否存在

        Args：
            key_id: 键
        Returns：
            bool: 键存在返回 True，否则返回 False
        """
        return await self.client.exists(key_id) > 0

redis_client = RedisConfig()
