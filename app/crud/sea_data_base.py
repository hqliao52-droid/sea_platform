from typing import Any, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD:
    """
    通用数据库操作基类
    所有模型的CRUD都继承这个类，自动获得 insert, update, delete, get 等方法
    注意：
        基类CRUD中不做任何异常处理，所有的异常都由service处理（事务回滚等）
    """

    def __init__(self, model):
        self.model = model

    async def insert(self, db: AsyncSession, obj) -> Optional[Any]:
        if isinstance(obj, dict):
            obj = self.model(**obj)

        db.add(obj)
        await db.flush()
        await db.refresh(obj)
        return obj

    async def update(
        self, db: AsyncSession, obj_id: int, update_data: dict
    ) -> Optional[Any]:
        obj = await self.get(db, obj_id)
        if not obj:
            return None

        for k, v in update_data.items():
            if hasattr(obj, k):
                setattr(obj, k, v)

        await db.flush()
        await db.refresh(obj)
        return obj

    async def delete(self, db: AsyncSession, obj_id: int) -> Optional[Any]:
        obj = await self.get(db, obj_id)
        if obj:
            await db.delete(obj)
        return obj

    async def get(self, db: AsyncSession, obj_id: int) -> Optional[Any]:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession):
        stmt = select(self.model)
        result = await db.execute(stmt)
        return result.scalar().all()
