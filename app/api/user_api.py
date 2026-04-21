from fastapi import APIRouter, Request,Body,Header
from app.utils.jwt import create_access_token,hash_password,verify_password
from app.services.user_service import UserService
from app.utils.result_response import Result
from app.utils.result_response import ResultCode
from app.utils.ip_util import get_real_ip
from app.schemas.user.user_schema import UserSchema
from app.schemas.user.user_response_schema import UserResponseSchema
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

    print(f"用户信息：{user_info}")

    if user_info["status"] == "fail":
        return Result.error(ResultCode.USER_NOT_EXIST_ERROR)

    stored_user = user_info["user"]

    if not verify_password(password, stored_user.password):
        return Result.error(ResultCode.USER_ACCOUNT_ERROR)
    
    # if password != verify_token(stored_user.password):
    #     return Result.error(ResultCode.USER_ACCOUNT_ERROR)
    user_id = user_info["user"].id
    print(f"用户ID：{user_id}")
        
    
    ip = get_real_ip(request)
    if ip:
        update_data = {"last_login_ip": ip}
        user_service.update_user(user_id,update_data)
        stored_user.last_login_ip = ip
    
    token = create_access_token({"username": username})
    
    user_response = UserResponseSchema.model_validate(stored_user)
    return Result.success(data={"token": token,
                                "token_type": "bearer",
                                "userInfo":user_response})

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
    user_model.status = 1
    user_model.role = "user"

    result = user_service.insert_user(user_model)

    if result["status"] == "success":
        return Result.success(data={"message": "注册成功"})
    else:
        return Result.error(ResultCode.USER_REGISTER_ERROR)

@router.post("/logout")
def logout(authorization: str = Header(None)):
    token = authorization.replace("Bearer ", "")
    redis.init_black_list_token(token)
    return Result.success()






