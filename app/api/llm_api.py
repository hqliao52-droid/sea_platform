from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter
from app.clients.llm_client import get_DouBao_stream_output

router = APIRouter()    
@router.get("/llm_stream")
async def stream_response(query: str):
    return EventSourceResponse(
        get_DouBao_stream_output(query),  # 传入生成器
    )