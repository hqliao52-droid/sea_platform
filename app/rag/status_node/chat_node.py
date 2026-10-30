from app.config.redis_config import RedisConfig


class ChatNode:
    def __init__(self):
        self.redis_client = RedisConfig()

    async def analyzing(self, task_id: str):
        await self.redis_client.append_stream(task_id, "[[STATUS:analyzing]]")

    async def retrieving(self, task_id: str):
        await self.redis_client.append_stream(task_id, "[[STATUS:retrieving]]")

    async def generating(self, task_id: str):
        await self.redis_client.append_stream(task_id, "[[STATUS:generating]]")

    async def reading(self, task_id: str):
        await self.redis_client.append_stream(task_id, "[[STATUS:reading]]")

    async def done(self, task_id: str):
        await self.redis_client.append_stream(task_id, "[[STATUS:done]]")

    async def error(self, task_id: str):
        await self.redis_client.append_stream(task_id, "[[STATUS:error]]")

    async def end(self, task_id: str):
        await self.redis_client.append_stream(task_id, "[[STATUS:end]]")
