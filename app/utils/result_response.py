from enum import Enum
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel,ValidationError

T = TypeVar("T")


# 对应 Java 的 ResultCode 枚举
class ResultCode(Enum):
    SUCCESS = ("200", "成功")
    PARAM_ERROR = ("400", "参数异常")
    TOKEN_INVALID_ERROR = ("401", "未登录")
    TOKEN_CHECK_ERROR = ("402", "token验证失败，请重新登录")
    PARAM_LOST_ERROR = ("4001", "参数缺失")
    SYSTEM_ERROR = ("500", "系统异常")
    USER_EXIST_ERROR = ("5001", "用户名已存在")
    USER_NOT_LOGIN = ("5002", "用户未登录")
    USER_ACCOUNT_ERROR = ("5003", "账号或密码错误")
    USER_NOT_EXIST_ERROR = ("5004", "用户不存在")
    PARAM_PASSWORD_ERROR = ("5005", "原密码输入错误")
    USER_REGISTER_ERROR = ("5006", "用户注册失败,请稍后重试...")

    FILE_NOT_FOUND = ("5007", "文件不存在")

    MSG_NOT_EXIST_ERROR = ("6001", "消息不存在")


    JSON_ERROR = ("6000", "JSON解析错误")

    def __init__(self, code: str, msg: str | list):
        self.code = code
        self.msg = msg


# 对应 Java 的 Result<T>
class Result(BaseModel, Generic[T]):
    code: str
    msg: str | list
    data: Optional[T] = None

    # Result.success()
    @classmethod
    def success(cls, data: T = None, msg: str | list = None) -> "Result[T]":
        return cls(
            code=ResultCode.SUCCESS.code,
            msg=msg or ResultCode.SUCCESS.msg,
            data=data,
        )

    # Result.error() —— 支持传入任意 ResultCode
    @classmethod
    def error(
        cls, result_code: ResultCode = ResultCode.SYSTEM_ERROR, msg: str | list = None
    ) -> "Result[None]":
        return cls(
            code=result_code.code,
            msg=msg or result_code.msg,
            data=None,
        )
    
    @staticmethod
    def format_validation_error(e: ValidationError) -> str:
        """格式化 Pydantic 验证错误为可读字符串"""
        errors = []
        for error in e.errors():
            field_path = " -> ".join(str(loc) for loc in error["loc"])
            error_type = error["type"]
            error_msg = error["msg"]
            
            # 添加更多上下文
            if "missing" in error_type:
                errors.append(f"缺少必需字段: {field_path}")
            elif "type_error" in error_type:
                expected = error.get("ctx", {}).get("expected", "unknown")
                errors.append(f"字段 {field_path} 类型错误，期望 {expected}")
            else:
                errors.append(f"字段 {field_path}: {error_msg}")
        
        return "; ".join(errors)
