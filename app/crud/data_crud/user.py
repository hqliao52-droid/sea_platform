from app.crud.sea_data_base import BaseCRUD
from app.models.user_model import UserModel
from sqlalchemy.orm import Session

class UserCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(UserModel)

    def get_user_by_id(self,db:Session,user_id):
        return db.query(UserModel).filter(UserModel.id==user_id).first()