from langfuse.langchain import CallbackHandler
from langfuse import Langfuse
from langchain.agents.middleware import AgentMiddleware

from app.services.chat_session_service import ChatSessionOperator
from app.config.settings import settings
from app.config.redis_config import redis_client
from app.utils.utils import generate_id


chat_session_operator = ChatSessionOperator()

class TraceIDError(ValueError):
    """trace_id is not valid """

def set_langfuse_client(trace_id: str | None = None):
    _ = Langfuse(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        base_url=settings.LANGFUSE_BASE_URL,
        timeout=15,
    )

    _dict: dict = {}
    if trace_id: 
        _dict["trace_id"] = trace_id
    else:
        _dict["trace_id"] = generate_id(is_32bit=True)
    return CallbackHandler(trace_context=_dict)

async def get_trace_id(
        user_id : int | str | None = None, 
        session_id: int | None = None
    ):
    if not(session_id and user_id):
        raise TraceIDError("Get TRACE-ID:session_id and user_id must be provided")
    trace_id = await redis_client.get_trace_id(user_id, session_id)
    if not trace_id: 
        trace_id = generate_id(is_32bit=True)
        await set_trace_id(user_id, session_id, trace_id)
    return trace_id

async def set_trace_id(
        user_id: int | str , 
        session_id: int | str,
        trace_id: str
    ):
    if not(session_id and user_id):
        raise TraceIDError("Set TRACE-ID:session_id and user_id must be provided")
    if len(trace_id) != 32:
        raise TraceIDError("Set TRACE-ID:trace_id must be 32 characters")
    await redis_client.set_trace_id(user_id, session_id, trace_id)