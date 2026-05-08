from fastapi import Header
from app.utils.result_response import Result
from app.utils.result_response import ResultCode
from app.utils.jwt import verify_token
from app.config.redis_config import RedisConfig
from app.services.user_service import UserService

redis = RedisConfig()
user_service = UserService()

def get_current_user(authorization: str = Header(None)):
    """
    从请求头获取token并解析
    """

    if not authorization:
        return Result.error(ResultCode.USER_NOT_LOGIN)
    
    token = authorization.replace("Bearer ", "")

    if redis.check_black_list_token(token):
        return Result.error(ResultCode.TOKEN_CHECK_ERROR)

    payload = verify_token(token)
    if not payload:
        return Result.error(ResultCode.TOKEN_INVALID_ERROR)
    
    user_id = payload.get("sub")
    if not user_id:
        return Result.error(ResultCode.TOKEN_INVALID_ERROR)
    
    stored_user = user_service.get_user_by_id(user_id)
    if not stored_user:
        return Result.error(ResultCode.USER_NOT_EXIST_ERROR)
    
    return stored_user