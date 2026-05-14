from app.utils.logger import Logger
from app.config.mysql_config import db_session
from app.crud.sea_data_base import BaseCRUD
from app.crud.data_crud.user_push_config import UserPushConfigCRUD
from app.models.user_push_config import UserPushConfigModel
from app.schemas.user_push_config.user_push_config_schema import UserPushConfigSchema

class UserPushConfigService(BaseCRUD):
    def __init__(self):
        self.config_crud = UserPushConfigCRUD()
        self.logger = Logger.setup_logger(Logger.set_file_date())
    
    def get_by_user_id(
        self,
        user_id: int,
    ) -> UserPushConfigModel | None:
        db = db_session()
        try:
            return self.config_crud.get_by_user_id(db, user_id)
        except Exception as e:
            self.logger.error("查询用户推送配置失败:%s",str(e))
            return None
        finally:
            db.close()
    
    def insert(self,obj:UserPushConfigSchema):
        db = db_session()
        try:
            new_config = self.config_crud.insert(db,obj)
            db.commit()
            db.refresh(new_config)
            return new_config
        except Exception as e:
            self.logger.error("插入用户推送配置失败:%s",str(e))
            db.rollback()
        finally:
            db.close()
        
    def update_by_user_id(
        self, 
        user_id: int, 
        obj_in: UserPushConfigSchema
    ) -> UserPushConfigModel | None:
        db = db_session()
        try:
            db_obj = self.config_crud.get_by_user_id(db, user_id)
            if not db_obj:
                self.logger.warning("尝试更新不存在的用户配置: user_id=%d", user_id)
                return None
            updated_obj = self.config_crud.update(db, db_obj, obj_in)
            db.commit()
            db.refresh(updated_obj)
            self.logger.info("用户推送配置更新成功: user_id=%d", user_id)
            return updated_obj
        except Exception as e:
            self.logger.error("更新用户推送配置失败: user_id=%d, error=%s", user_id, str(e))
            db.rollback()
            raise e
        finally:
            db.close()