from app.utils.jwt import verify_token
from app.config.redis_config import RedisConfig
from app.services.user_service import UserService
from app.utils.logger import Logger
from app.models.user_model import UserModel

from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)


redis = RedisConfig()
user_service = UserService()

logger = Logger.setup_logger(Logger.set_file_date())

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> UserModel:
    """
    统一认证 -> 返回User对象
    """
    if credentials is None:
        logger.error("没有authorization")
        raise HTTPException(status_code=401, detail="未登录")

    token = credentials.credentials
    logger.info("token = %s***", token[:8]) 

    if await redis.check_black_list_token(token):
        logger.error("Token已失效")
        raise HTTPException(status_code=401, detail="Token已失效")

    payload = verify_token(token)
    logger.info(f"token = {token}")
    if not payload:
        logger.error("Token无效")
        raise HTTPException(status_code=401, detail="Token无效")

    user_id = payload.get("sub")
    if not user_id:
        logger.error("Token缺少sub")
        raise HTTPException(status_code=401, detail="Token缺少sub")

    user: UserModel = await user_service.get_user_by_id(int(user_id))
    if not user:
        logger.error("用户不存在")
        raise HTTPException(status_code=404, detail="用户不存在")
    logger.info(f"用户:{user.username} 登录,, token校验成功！！！")
    return user
