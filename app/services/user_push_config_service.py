from app.utils.logger import Logger
from app.config.mysql_config import AsyncSessionLocal
from app.crud.sea_data_base import BaseCRUD
from app.crud.data_crud.user_push_config import UserPushConfigCRUD
from app.models.user_push_config import UserPushConfigModel
from app.schemas.user_push_config.user_push_config_schema import UserPushConfigSchema
from app.schemas.user_push_config.user_push_config_schema import (
    UserPushConfigResponseSchema,
)


class UserPushConfigService(BaseCRUD):
    def __init__(self):
        self.config_crud = UserPushConfigCRUD()
        self.logger = Logger.setup_logger(Logger.set_file_date())

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> UserPushConfigModel | None:
        async with AsyncSessionLocal() as db:
            try:
                model = await self.config_crud.get_by_user_id(db, user_id)
                if not model:
                    return None
                response_data = UserPushConfigSchema.model_validate(model)
                return response_data
            except Exception as e:
                self.logger.error("查询用户推送配置失败:%s", str(e))
                return None

    async def insert(
        self, obj: UserPushConfigSchema
    ) -> UserPushConfigResponseSchema | None:
        async with AsyncSessionLocal() as db:
            try:
                new_config = await self.config_crud.insert(db, obj)
                await db.commit()
                # 插入成功后显式刷新子表的数据
                await db.refresh(new_config, attribute_names=["channels", "weights"])
                result = UserPushConfigResponseSchema.model_validate(new_config)
                return result
            except Exception as e:
                self.logger.error("插入用户推送配置失败:%s", str(e))
                await db.rollback()
                raise e

    async def update_by_user_id(
        self, user_id: int, obj_in: UserPushConfigSchema
    ) -> UserPushConfigResponseSchema | None:
        async with AsyncSessionLocal() as db:
            try:
                db_obj = await self.config_crud.get_by_user_id(db, user_id)
                if not db_obj:
                    self.logger.warning("尝试更新不存在的用户配置: user_id=%d", user_id)
                    return None
                updated_obj = await self.config_crud.update(db, db_obj, obj_in)
                
                await db.refresh(updated_obj, attribute_names=["channels", "weights"])
                await db.commit()
                # 插入成功后显式刷新子表的数据
                self.logger.info("用户推送配置更新成功: user_id=%d", user_id)
                result = UserPushConfigResponseSchema.model_validate(updated_obj)
                return result
            except Exception as e:
                self.logger.error(
                    "更新用户推送配置失败: user_id=%d, error=%s", user_id, str(e)
                )
                await db.rollback()
                raise e
