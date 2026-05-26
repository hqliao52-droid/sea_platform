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
    
    def get_user_by_username(self,username:str):
        db = db_session()
        try:
            user = self.user_crud.get_user_by_username(db,username)
            if user:
                return {"user":user,"status":"success"}
            else:
                return {"user":None,"status":"fail"}
        except Exception as e:
            self.logger.error("查询用户失败:%s",str(e))
        finally:
            db.close()
    def verify_phone(self,phone:int):
        db = self.db_session()
        try:
            user = self.user_crud.get_user_by_phone(db,phone)
            return user
        except Exception as e:
            self.logger.error("查询用户失败:%s",str(e))
            return None
        finally:
            db.close()
    
    def update_user_password(self,id:int,new_password:str):
        db = db_session()
        try:
            self.logger.info("更新用户密码:%s",id)
            updated_id = self.user_crud.update(db,id,{"password":new_password})
            if updated_id:
                return True
            else:
                return False
        except Exception as e:
            self.logger.error("更新用户密码失败:%s",str(e))
        finally:
            db.close()


    def get_user_by_id(self,id:int):
        db = db_session()
        try: 
            user = self.user_crud.get(db,id)
            if user:
                return user
            else:
                return None
        except Exception as e:
            self.logger.error("查询用户失败:%s",str(e))
        finally:
            db.close()


    def update_user(self,id:int,user_data:dict):
        """更新（部分更新）"""
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

    def update_user_info(self,id:int,user_data:dict):
        db = db_session()
        self.logger.info("更新用户信息:%s",user_data)
        try:
            user = self.user_crud.get(db,id)
            if not user:
                return {"user":None,"status":"fail","msg":"用户不存在"}
            
            update_date = user_data.model_dump(exclude_unset=True)
            updated = self.user_crud.update_segment(db,id,update_date)

            return {"user":updated,"status":"success","msg":"更新成功"}
        except Exception as e:
            self.logger.error("更新用户失败:%s",str(e))
            db.rollback()
            return {"user":None,"status":"fail","msg":f"出现异常：{str(e)}"}
        
        finally:
            db.close()

