from fastapi import Header, HTTPException

from app.utils.jwt import verify_token
from app.config.redis_config import RedisConfig
from app.services.user_service import UserService


redis = RedisConfig()
user_service = UserService()


def get_current_user(
        authorization: str = Header(None)
):
    """
    获取当前登录用户
    """

    # 未登录
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="用户未登录"
        )

    # Bearer token
    token = authorization.replace(
        "Bearer ",
        ""
    )

    # Redis黑名单校验
    if redis.check_black_list_token(token):
        raise HTTPException(
            status_code=401,
            detail="Token已失效"
        )

    # JWT解析
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token无效"
        )

    # 获取用户ID
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Token缺少sub"
        )

    '''
    注意：

    这里必须返回：
        User ORM对象

    不能返回：
        Result对象
    '''
    stored_user = user_service.get_user_by_id(
        int(user_id)
    )

    if not stored_user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )

    return stored_user