import json
from app.config.redis_config import redis_client


class AgentOrchestrator:

    def __init__(self, task_id):
        self.task_id = task_id

    def emit_status(self, state, text):
        redis_client.client.lpush(
            f"stream:{self.task_id}",
            json.dumps({"type": "status", "state": state, "text": text}),
        )

    def emit_delta(self, chunk):
        redis_client.client.lpush(
            f"stream:{self.task_id}", json.dumps({"type": "delta", "content": chunk})
        )

    def emit_done(self):
        redis_client.client.lpush(
            f"stream:{self.task_id}", json.dumps({"type": "done"})
        )
