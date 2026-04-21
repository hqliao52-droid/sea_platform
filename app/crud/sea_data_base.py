from sqlalchemy.orm import Session
from app.config.mysql_config import SessionLocal

class BaseCRUD:
    """
    通用数据库操作基类
    所有模型的CRUD都继承这个类，自动获得 insert, update, delete, get 等方法
    """
    def __init__(self, model):
        self.model = model

    def insert(self, db: Session, obj):
        if isinstance(obj, dict):
            obj = self.model(**obj)

        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj_id: int, update_data: dict):
        obj = db.query(self.model).filter(self.model.id == obj_id).first()
        if not obj:
            return None

        for k, v in update_data.items():
            setattr(obj, k, v)

        db.commit()
        db.refresh(obj)
        return obj
    
    def update_segment(self, db: Session, id: int, update_data: dict):
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            return None
        
        # 遍历字典，只更新存在的键值对
        for key,value in update_data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj_id: int):
        obj = db.query(self.model).filter(self.model.id == obj_id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    
    def get(self, db: Session, obj_id: int):
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(self, db: Session):
        return db.query(self.model).all()