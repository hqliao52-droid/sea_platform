from fastapi import APIRouter
from app.utils.result_response import Result
from app.services.category_service import CategoryOperator
from app.schemas.category.category import categoryBase as categorySchema
from app.utils.logger import Logger
from typing import List

router = APIRouter()
logger = Logger.setup_logger(Logger.set_file_date())

@router.get("/get_category", response_model=Result[List[categorySchema]])
async def get_category_is_active():
    """获取所有有效的分类"""
    category_operator = CategoryOperator()
    data = category_operator.get_category_is_active()
    result = [categorySchema.from_orm(item) for item in data]

    return Result.success(result)

@router.get("/get_category_by_id", response_model=Result[categorySchema])
async def get_category_by_id(id: int):
    """根据id获取分类"""
    category_operator = CategoryOperator()
    data = category_operator.get_category_by_id(id)
    result = categorySchema.from_orm(data)

    return Result.success(result)
