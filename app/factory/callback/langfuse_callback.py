from langfuse.langchain import CallbackHandler
from langfuse import Langfuse
from langchain.agents.middleware import AgentMiddleware

from app.config.settings import settings
from app.utils.utils import generate_id

def set_langfuse_client(trace_id: str | None = None):
    _ = Langfuse(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        base_url=settings.LANGFUSE_BASE_URL,
        timeout=15,
    )

    trace_context = {"trace_id": trace_id} if trace_id else generate_id()
    return CallbackHandler(trace_context=trace_context)