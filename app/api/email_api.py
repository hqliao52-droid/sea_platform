from fastapi import APIRouter,Depends
from app.utils.result_response import Result, ResultCode
from app.schemas.email_SMTP.email_smtp_schema import EmailRequest, VerifyCodeRequest
from app.services.email_service import EmailService
from app.core.user_deps import get_current_user

router = APIRouter()
@router.post("/send_code", response_model=Result)
async def send_code(reqEmail: EmailRequest,user_info=Depends(get_current_user)):
    user_id = user_info.id
    user_name = user_info.username
    EmailService.send_verification_code(reqEmail.email,user_id=user_id,user_name=user_name)
    return Result.success(data="验证码已发送！",msg="验证码已发送！")

@router.post("/verify_code", response_model=Result)
async def verify_code(req: VerifyCodeRequest,user_info=Depends(get_current_user)):
    success = EmailService.verify_code(req.email,user_id=user_info.id,user_name=user_info.username,code=req.code)
    if not success:
        return Result.error(ResultCode.PARAM_ERROR,msg="验证码错误或已过期")
    
    return Result.success(data="验证成功",msg="验证成功")

@router.post("/register/send_code", response_model=Result)
async def register_send_code(reqEmail: EmailRequest):
    """注册时发送验证码"""
    # 1. 可选：检查邮箱是否已存在，如果已存在则提示直接登录或找回密码
    # 2. 发送验证码，此时 user_id 和 user_name 可以为 None 或默认值
    EmailService.send_register_verification_code(reqEmail.email)
    return Result.success(data="验证码已发送！", msg="验证码已发送！")

@router.post("/register/verify_code", response_model=Result)
async def register_verify_code(req: VerifyCodeRequest):
    """注册时验证验证码"""
    # 验证逻辑可能需要调整，因为此时没有 user_id
    # 建议在 EmailService.verify_code 中支持 user_id 为 None 的情况
    success = EmailService.register_verify_code(req.email, code=req.code)
    if not success:
        return Result.error(ResultCode.PARAM_ERROR, msg="验证码错误或已过期")
    
    # 验证成功后，可以返回一个临时的 ticket 或标记，供注册接口使用，防止重放攻击
    return Result.success(data="验证成功", msg="验证成功")