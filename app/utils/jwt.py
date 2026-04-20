from datetime import datetime,timedelta
from jose import jwt
from app.config.settings import settings
from passlib.context import CryptContext

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
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)