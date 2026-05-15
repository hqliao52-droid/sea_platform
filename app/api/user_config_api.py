from fastapi import APIRouter, Depends
from app.utils.result_response import Result
from app.utils.result_response import ResultCode
from app.schemas.user_push_config.user_push_config_schema import UserPushConfigSchema,UserPushConfigResponseSchema
from app.services.user_push_config_service import UserPushConfigService
from app.core.user_deps import get_current_user

router = APIRouter()

@router.post("/get_config", response_model=Result[UserPushConfigSchema])
async def get_config(user_info=Depends(get_current_user)):
    if not user_info:
        return Result.error(result_code=ResultCode.TOKEN_INVALID_ERROR, msg="未登录")
    
    service = UserPushConfigService()

    config_model = service.get_by_user_id(user_info.id)
    if not config_model:
        return Result.success(data=None, msg="暂无配置，请先创建")
    
    try:
        response_data = UserPushConfigSchema.model_validate(config_model)
        return Result.success(data=response_data)
    except Exception as e:
        # 如果映射失败（通常是因为 Schema 字段和 Model 属性名不匹配），捕获异常
        return Result.error(result_code=ResultCode.SYSTEM_ERROR, msg=f"数据格式化失败: {str(e)}")

@router.put("/insert_config", response_model=Result[UserPushConfigResponseSchema])
async def insert_config(config: UserPushConfigSchema, user_info=Depends(get_current_user)):
    if not user_info:
        return Result.error(result_code=ResultCode.TOKEN_INVALID_ERROR, msg="未登录")
    
    service = UserPushConfigService()
    config.user_id = user_info.id
    config_model = service.insert(config)
    try:
        response_data = UserPushConfigResponseSchema.model_validate(config_model)
        return Result.success(data=response_data)
    except ValueError as e:
        # 如果映射失败（通常是因为 Schema 字段和 Model 属性名不匹配），捕获异常
        error_msg = Result.format_validation_error(e)
        return Result.error(result_code=ResultCode.SYSTEM_ERROR, msg=f"数据验证失败:  {error_msg}")
    except Exception as e:
        # 如果映射失败（通常是因为 Schema 字段和 Model 属性名不匹配），捕获异常
        return Result.error(result_code=ResultCode.SYSTEM_ERROR, msg=f"数据格式化失败: {str(e)}")
    

@router.put("/update_config", response_model=Result[UserPushConfigResponseSchema])
async def update_config(config: UserPushConfigSchema, user_info=Depends(get_current_user)):
    if not user_info:
        return Result.error(result_code=ResultCode.TOKEN_INVALID_ERROR, msg="未登录")
    
    service = UserPushConfigService()
    config.user_id = user_info.id
    config_model = service.update(config)
    try:
        response_data = UserPushConfigResponseSchema.model_validate(config_model)
        return Result.success(data=response_data)
    except Exception as e:
        # 如果映射失败（通常是因为 Schema 字段和 Model 属性名
        return Result.error(result_code=ResultCode.SYSTEM_ERROR, msg=f"数据格式化失败: {str(e)}")
