import random
from app.config.redis_config import redis_client
from app.tasks.email_sender import send_email

class EmailService:
    CODE_EXPIRE_SECONDS = 300

    @staticmethod
    def generate_code() -> str:
        return str(random.randint(100000, 999999))
    
    @staticmethod
    def send_verification_code(email: str, user_id: int, user_name:str) -> str:
        code = EmailService.generate_code()
        key = f"email:{user_id}:{user_name}:{email}"
        redis_client.set_key(key, code, EmailService.CODE_EXPIRE_SECONDS)
        send_email(to_email=email, subject="Verification Code", content=f"Your verification code is: {code}, 5 minutes later, the verification code will expire. Please do not share your verification code with others.")
        return code
    
    @staticmethod
    def verify_code(email: str, user_id: int, user_name:str, code: str) -> bool:
        key = f"email:{user_id}:{user_name}:{email}"
        stored_code = redis_client.get_key(key)

        if not stored_code:
            return False
        
        if stored_code != code:
            return False
        
        # redis_client.delete_key(key)
        return True