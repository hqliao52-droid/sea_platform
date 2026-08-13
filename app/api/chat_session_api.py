from fastapi import APIRouter,Body,Depends
from typing import List

from app.utils.result_response import Result
from app.utils.result_response import ResultCode
from app.utils.ip_util import get_real_ip
from app.services.chat_session_service import ChatSessionOperator
from app.schemas.chat_session.chat_session import ChatSessionSchema
from app.core.user_deps import get_current_user
from app.utils.logger import Logger

chat_session_router = APIRouter()

chat_session_operator = ChatSessionOperator()
logger = Logger.setup_logger(Logger.set_file_date())

@chat_session_router.get("/get_sessions", response_model=Result[List[ChatSessionSchema]])
async def get_chat_session_by_llm_id(user_id: int):
    """通过userID获取会话列表"""
    session = chat_session_operator.get_chat_session_by_user_id(user_id)
    if session is not None:
        return Result.success(session)
    else:
        return Result.error(ResultCode.SYSTEM_ERROR)

@chat_session_router.put("/new_session")
async def new_session(user=Depends(get_current_user)):
    from app.config.mysql_config import db_session
    db = db_session()
    try:
        select_session = await chat_session_operator.get_new_chat_session_by_user_id(db,user.id)
        logger.info(f"用户:{user} 新建会话")
        if select_session is not None:
            logger.info(f"用户ID:{user.id} 新建会话成功")
            return Result.success(select_session)
        else:
            return Result.error(ResultCode.SYSTEM_ERROR)
    except Exception as e:
        logger.error(e)
        return Result.error(ResultCode.SYSTEM_ERROR)
    finally:
        db.close()
