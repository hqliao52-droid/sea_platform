from enum import Enum
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar("T")


# 对应 Java 的 ResultCode 枚举
class ResultCode(Enum):
    SUCCESS = ("200", "成功")
    PARAM_ERROR = ("400", "参数异常")
    TOKEN_INVALID_ERROR = ("401", "无效的token")
    TOKEN_CHECK_ERROR = ("401", "token验证失败，请重新登录")
    PARAM_LOST_ERROR = ("4001", "参数缺失")
    SYSTEM_ERROR = ("500", "系统异常")
    USER_EXIST_ERROR = ("5001", "用户名已存在")
    USER_NOT_LOGIN = ("5002", "用户未登录")
    USER_ACCOUNT_ERROR = ("5003", "账号或密码错误")
    USER_NOT_EXIST_ERROR = ("5004", "用户不存在")
    PARAM_PASSWORD_ERROR = ("5005", "原密码输入错误")
    USER_REGISTER_ERROR = ("5006", "用户注册失败,请稍后重试...")

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
