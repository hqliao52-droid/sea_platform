from fastapi import APIRouter,Depends
from app.services.ai_service import ai_service
from fastapi.responses import StreamingResponse
from app.core.user_deps import get_current_user
from app.utils.logger import Logger

router = APIRouter()    

logger = Logger.setup_logger(Logger.set_file_date())
 
@router.get("/llm_stream")
async def stream_response(query: str,user=Depends(get_current_user)):
    logger.info(f"用户{user}请求LLM服务，查询内容：{query}")
    llm = ai_service.DouBaoSeedLite(query)
    return StreamingResponse(llm, media_type="text/plain;charset=utf-8")