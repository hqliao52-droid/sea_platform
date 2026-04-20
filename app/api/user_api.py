from fastapi import APIRouter, Request,Body,Header
from app.utils.jwt import create_access_token,hash_password,verify_token
from app.services.user_service import UserService
from app.utils.result_response import Result
from app.utils.result_response import ResultCode
from app.utils.ip_util import get_real_ip
from app.schemas.user.user_schema import UserSchema
from app.models.user_model import UserModel
from app.config.redis_config import RedisConfig

router = APIRouter()

redis = RedisConfig()

@router.post("/login")
def login(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    request: Request = None
):
    user_service = UserService()
    user_info = user_service.get_user_by_username(username)

    print(user_info)

    if user_info["status"] == "fail":
        return Result.error(ResultCode.USER_NOT_EXIST_ERROR)

    stored_user = user_info["user"]

    if user_info["status"] == "success":
        if password != verify_token(stored_user.password):
            return Result.error(ResultCode.USER_ACCOUNT_ERROR)
        
    
    ip = get_real_ip(request)
    if ip:
        stored_user.last_login_ip = ip
        user_service.update_user(stored_user.id,stored_user)
    
    token = create_access_token({"username": username})

    return Result.success(data={"token": token,"token_type": "bearer"})

@router.post("/register")
def register(user: UserSchema,request: Request = None):
    user_service = UserService()
    user_info = user_service.get_user_by_username(user.username)
    if user_info["status"] == "success":
        return Result.error(ResultCode.USER_EXIST_ERROR)
    
    hashed_pwd = hash_password(user.password)
    ip = get_real_ip(request)
    user_model = UserModel()
    user_model.username = user.username
    user_model.password = hashed_pwd
    user_model.avatar = user.avatar or None
    user_model.nickname = user.nickname or None
    user_model.phone = user.phone or None
    user_model.email = user.email or None
    user_model.city = user.city or None
    user_model.last_login_ip = ip or None

    result = user_service.insert_user(user_model)

    if result["status"] == "success":
        return Result.success(data={"message": "注册成功"})
    else:
        return Result.error(ResultCode.USER_REGISTER_ERROR)

@router.get("/logout")
def logout(request: Request,authorization: str = Header(None)):
    token = authorization.replace("Bearer ", "")
    redis.init_black_list_token(token)
    return Result.success(data={"message": "退出成功！"})






