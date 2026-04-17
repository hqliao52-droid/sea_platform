from app.utils.logger import Logger
from app.models.user_model import UserModel
from app.crud.data_crud.user import UserCRUD
from app.config.mysql_config import db_session

class UserService:
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.user_crud = UserCRUD()

    def insert_user(self,user:UserModel):
        db = db_session()
        try:
            id = self.user_crud.insert(db,user)
            if id:
                return {"id":id,"status":"success"}
            else:
                return {"id":None,"status":"fail"}
        except Exception as e:
            self.logger.error("插入用户失败:%s",str(e))
        finally:
            db.close()
    
    def get_user_by_id(self,id:int):
        db = db_session()
        try:
            user = self.user_crud.get_user_by_id(db,id)
            if user:
                return {"user":user,"status":"success"}
            else:
                return {"user":None,"status":"fail"}
        except Exception as e:
            self.logger.error("查询用户失败:%s",str(e))
        finally:
            db.close()
