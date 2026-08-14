import random
from app.config.redis_config import redis_client
from app.tasks.email_sender import send_email

class EmailService:
    CODE_EXPIRE_SECONDS = 300

    @staticmethod
    def generate_code() -> str:
        return str(random.randint(100000, 999999))
    
    @staticmethod
    async def send_verification_code(email: str, user_id: int, user_name:str) -> str:
        code = EmailService.generate_code()
        key = f"email:{user_id}:{user_name}:{email}"
        await redis_client.set_key(key, code, EmailService.CODE_EXPIRE_SECONDS)
        await send_email(to_email=email, subject="Verification Code", content=f"Your verification code is: {code}, 5 minutes later, the verification code will expire. Please do not share your verification code with others.")
        return code
    
    @staticmethod
    async def verify_code(email: str, user_id: int, user_name:str, code: str) -> bool:
        key = f"email:{user_id}:{user_name}:{email}"
        stored_code = await redis_client.get_key(key)

        if not stored_code:
            return False
        
        if stored_code != code:
            return False
        
        # redis_client.delete_key(key)
        return True
    
    @staticmethod
    async def send_register_verification_code(email: str) -> str:
        code = EmailService.generate_code()
        email_account = email.split("@")[0]
        key = f"email:{email_account}:{email}"
        await redis_client.set_key(key, code, EmailService.CODE_EXPIRE_SECONDS)
        await send_email(to_email=email, subject="Verification Code", content=f"Your verification code is: {code}, 5 minutes later, the verification code will expire. Please do not share your verification code with others.")
        return code
    
    @staticmethod
    async def register_verify_code(email: str, code: str) -> bool:
        email_account = email.split("@")[0]
        key = f"email:{email_account}:{email}"
        stored_code = await redis_client.get_key(key)

        if not stored_code:
            return False
        
        if stored_code != code:
            return False
        
        # redis_client.delete_key(key)
        return True