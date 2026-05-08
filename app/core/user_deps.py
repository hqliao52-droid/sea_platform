from fastapi import Header, HTTPException
from app.utils.jwt import verify_token
from app.config.redis_config import RedisConfig
from app.services.user_service import UserService

redis = RedisConfig()
user_service = UserService()


def get_current_user(authorization: str = Header(None)):
    """
    统一认证：只做一件事 -> 返回User对象
    """

    if not authorization:
        raise HTTPException(status_code=401, detail="未登录")

    token = authorization.replace("Bearer ", "")

    if redis.check_black_list_token(token):
        raise HTTPException(status_code=401, detail="Token已失效")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token无效")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token缺少sub")

    user = user_service.get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    return user