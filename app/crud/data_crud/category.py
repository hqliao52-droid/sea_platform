from app.crud.sea_data_base import BaseCRUD
from app.models.category import category
from sqlalchemy.orm import Session

class CategoryCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(category)

    def get_category_is_active(self, db: Session):
        return db.query(category).filter(category.is_active == 1).all()
        