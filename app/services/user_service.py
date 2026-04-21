from app.utils.logger import Logger
from app.models.user_model import UserModel
from app.crud.data_crud.user import UserCRUD
from app.config.mysql_config import db_session
from app.schemas.user.user_schema import UserSchema

class UserService:
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.user_crud = UserCRUD()

    def insert_user(self,user:UserModel):
        db = db_session()
        try:
            self.logger.info("插入用户:%s",user.username)
            id = self.user_crud.insert(db,user)
            if id:
                return {"id":id,"status":"success"}
            else:
                return {"id":None,"status":"fail"}
        except Exception as e:
            self.logger.error("插入用户失败:%s",str(e))
        finally:
            db.close()
    
    def get_user_by_username(self,username:int):
        db = db_session()
        try:
            user = self.user_crud.get_user_by_id(db,username)
            if user:
                return {"user":user,"status":"success"}
            else:
                return {"user":None,"status":"fail"}
        except Exception as e:
            self.logger.error("查询用户失败:%s",str(e))
        finally:
            db.close()

    def update_user(self,id:int,user_data:dict):
        """更新（部分更新）"""
        print(f"更新后的信息：{user_data}")
        db = db_session()
        try:
            updated_id  = self.user_crud.update_segment(db,id,user_data)
            if updated_id:
                self.logger.info("更新用户成功:%s",updated_id)
                return {"id":updated_id,"status":"success"}
            else:
                return {"id":None,"status":"fail"}
        except Exception as e:
            self.logger.error("更新用户失败:%s",str(e))
            db.rollback()
            return {"id":None,"status":"fail"}
        finally:
            db.close()

