from fastapi import Header, HTTPException
from app.utils.jwt import verify_token
from app.config.redis_config import RedisConfig
from app.services.user_service import UserService
from app.utils.logger import Logger

redis = RedisConfig()
user_service = UserService()

logger = Logger.setup_logger(Logger.set_file_date())

def get_current_user(authorization: str = Header(None)):
    """
    统一认证：只做一件事 -> 返回User对象
    """

    if not authorization:
        logger.error("没有authorization")
        raise HTTPException(status_code=401, detail="未登录")

    token = authorization.replace("Bearer ", "")

    if redis.check_black_list_token(token):
        logger.error("Token已失效")
        raise HTTPException(status_code=401, detail="Token已失效")

    payload = verify_token(token)
    logger.info("token =", token)
    if not payload:
        logger.error("Token无效")
        raise HTTPException(status_code=401, detail="Token无效")

    user_id = payload.get("sub")
    if not user_id:
        logger.error("Token缺少sub")
        raise HTTPException(status_code=401, detail="Token缺少sub")

    user = user_service.get_user_by_id(int(user_id))
    if not user:
        logger.error("用户不存在")
        raise HTTPException(status_code=404, detail="用户不存在")

    return user