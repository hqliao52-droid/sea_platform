from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.sea_data_base import BaseCRUD
from app.models.user_model import UserModel


class UserCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(UserModel)

    async def get_user_by_username(self, db: AsyncSession, username: str) -> UserModel:
        try:
            stmt = select(UserModel).where(UserModel.username == username)
            result = await db.execute(stmt)
            user = result.scalars().first()
            return user
        except Exception as e:
            print("[获取用户信息失败]:", e)
            return None
    async def get_user_by_phone(self, db: AsyncSession, phone: int) -> UserModel:
        try:
            stmt = select(UserModel).where(UserModel.phone == phone)
            result = await db.execute(stmt)
            user = result.scalars().first()
            return user
        except Exception as e:
            raise e
