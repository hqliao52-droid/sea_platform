from fastapi import APIRouter, Depends
from typing import Annotated

from app.services.ai_service import ai_service
from app.core.user_deps import get_current_user
from app.utils.log import logger
from app.models.user_model import UserModel
from app.utils.utils import SSEStream, SSEEvent
from app.schemas.request.chat_request import ChatRequest
from app.services.chat_session_service import ChatSessionOperator

router = APIRouter()

chat_session_operator = ChatSessionOperator()

@router.post("/llm_stream_test")
async def stream_response(request: ChatRequest, user: UserModel = Depends(get_current_user)):
    if request.session_id is None:
        session = await chat_session_operator.new_chat_session_by_user_id(
            user.id
        )
        if session is not None:
            request.session_id = session.id

    yield SSEEvent.metadata(field="session_id", content=request.session_id)
    llm = ai_service.chat_ai_test(request, user)
    yield SSEStream.create_response(llm)


@router.get("/llm_stream_chat")
async def stream_response_chat(query: str):
    logger.info(f"用户请求LLM服务，内容：{query}")
