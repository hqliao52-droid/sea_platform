from datetime import datetime,timedelta
from jose import jwt
from app.config.settings import settings
from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def create_access_token(data: dict):
    """ 生成JWT TOKEN
    data: 需要存入token的数据，如：userId
    """
    to_encode = data.copy()
    # 设置token过期时间
    expire = datetime.utcnow() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # 生成token
    token = jwt.encode(to_encode,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)
    return token

def verify_token(token: str):
    """ 验证token
    token: 需要验证的token
    """
    try:
        payload = jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=[settings.JWT_ALGORITHM])
        return payload
    except Exception as e:
        return None

def hash_password(password: str) -> str:
    """ 对密码进行哈希处理
    password: 需要处理的密码
    """
    # print("🔥 进入新的 hash_password")
    # hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # print("原始长度:", len(password.encode('utf-8')))
    # print("sha256长度:", len(hashed_password.encode('utf-8')))
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ 验证密码 """
    # 同样先 SHA-256 处理输入密码
    # processed_password = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return pwd_context.verify(plain_password, hashed_password)