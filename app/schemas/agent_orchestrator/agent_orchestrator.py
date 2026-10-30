import json
from app.config.redis_config import redis_client


class AgentOrchestrator:

    def __init__(self, task_id):
        self.task_id = task_id

    async def emit_status(self, state, text):
        await redis_client.client.lpush(
            f"stream:{self.task_id}",
            json.dumps({"type": "status", "state": state, "text": text}),
        )

    async def emit_delta(self, chunk):
        await redis_client.client.lpush(
            f"stream:{self.task_id}", json.dumps({"type": "delta", "content": chunk})
        )

    async def emit_done(self):
        await redis_client.client.lpush(
            f"stream:{self.task_id}", json.dumps({"type": "done"})
        )
