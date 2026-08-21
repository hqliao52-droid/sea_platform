from app.config.redis_config import RedisConfig


class ChatNode:
    def __init__(self):
        self.redis_client = RedisConfig()

    def analyzing(self, task_id: str):
        self.redis_client.append_stream(task_id, "[[STATUS:analyzing]]")

    def retrieving(self, task_id: str):
        self.redis_client.append_stream(task_id, "[[STATUS:retrieving]]")

    def generating(self, task_id: str):
        self.redis_client.append_stream(task_id, "[[STATUS:generating]]")

    def reading(self, task_id: str):
        self.redis_client.append_stream(task_id, "[[STATUS:reading]]")

    def done(self, task_id: str):
        self.redis_client.append_stream(task_id, "[[STATUS:done]]")

    def error(self, task_id: str):
        self.redis_client.append_stream(task_id, "[[STATUS:error]]")

    def end(self, task_id: str):
        self.redis_client.append_stream(task_id, "[[STATUS:end]]")
