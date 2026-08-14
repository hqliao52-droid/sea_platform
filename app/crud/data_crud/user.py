from app.crud.sea_data_base import BaseCRUD
from app.models.user_model import UserModel
from sqlalchemy.orm import Session

class UserCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(UserModel)

    async def get_user_by_username(self,db:Session,username) -> UserModel:
        return await db.query(UserModel).filter(UserModel.username==username).first()
    
    async def get_user_by_phone(self,db:Session,phone) -> UserModel:
        return await db.query(UserModel).filter(UserModel.phone==phone).first()