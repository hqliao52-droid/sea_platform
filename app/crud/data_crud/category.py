from app.crud.sea_data_base import BaseCRUD
from app.models.category import category

class CategoryCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(category)
    
    def get_category_is_active(self) -> list[category]:
        try:
            return self.db.query(category).filter(category.is_active == 1).all()
        except Exception as e:
            self.logger.error(e)
        finally:
            self.db.close()
            self.close()
        