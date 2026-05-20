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
    EmailService.send_verification_code(reqEmail,user_id=user_id,user_name=user_name)
    return Result.success(data="验证码已发送！",msg="验证码已发送！")

@router.post("/verify_code", response_model=Result)
async def verify_code(req: VerifyCodeRequest,user_info=Depends(get_current_user)):
    success = EmailService.verify_code(req.email,user_id=user_info.id,user_name=user_info.username,code=req.code)
    if not success:
        return Result.error(ResultCode.PARAM_ERROR,msg="验证码错误或已过期")
    
    return Result.success(data="验证成功",msg="验证成功")