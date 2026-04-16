from app.crud.sea_data_base import BaseCRUD
from app.models.article_storage import ArticleStorage
from sqlalchemy.orm import Session

class CategoryCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(ArticleStorage)

    def get_by_id(self, db: Session, obj_id: int) -> ArticleStorage:
        return db.query(ArticleStorage).filter(ArticleStorage.id == obj_id).first()

    def get_by_article_name(self, db: Session, article_name: str) -> ArticleStorage:
        return db.query(ArticleStorage).filter(ArticleStorage.article_name == article_name).first()
    