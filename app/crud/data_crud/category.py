from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.sea_data_base import BaseCRUD
from app.models.category import Category


class CategoryCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(Category)

    async def get_category_is_active(self, db: AsyncSession):
        stmt = select(Category).where(Category.is_active == 1)
        result = await db.execute(stmt)
        return result.scalars().all()
