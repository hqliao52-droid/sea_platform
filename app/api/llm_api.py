from fastapi import APIRouter,Depends
from app.services.ai_service import ai_service
from fastapi.responses import StreamingResponse
from app.core.user_deps import get_current_user

router = APIRouter()    
@router.get("/llm_stream")
async def stream_response(query: str,user=Depends(get_current_user)):
    llm = ai_service.DouBaoSeedLite(query)
    return StreamingResponse(llm, media_type="text/plain;charset=utf-8")