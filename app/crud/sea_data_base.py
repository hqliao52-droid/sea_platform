from sqlalchemy.orm import Session
from app.config.mysql_config import SessionLocal

class BaseCRUD:
    """
    通用数据库操作基类
    所有模型的CRUD都继承这个类，自动获得 insert, update, delete, get 等方法
    """
    def __init__(self, model):
        self.model = model  # 传入ORM模型，如News
        self.db: Session = SessionLocal()  # 一次创建，复用

    def insert(self, obj):
        """
        通用插入：传入字典 或 模型实例
        返回 插入后的对象
        """
        try:
            # 如果是字典，自动转成模型实例
            if isinstance(obj, dict):
                obj = self.model(**obj)

            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except Exception as e:
            self.db.rollback()
            raise e

    def update(self, obj_id: int, update_data: dict):
        """
        通用更新：根据ID更新字段
        """
        try:
            query = self.db.query(self.model).filter(self.model.id == obj_id)
            obj = query.first()
            if not obj:
                return None

            query.update(update_data)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, obj_id: int):
        """通用删除"""
        try:
            obj = self.db.query(self.model).get(obj_id)
            if obj:
                self.db.delete(obj)
                self.db.commit()
            return obj
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get(self, obj_id: int):
        """根据ID查询单条"""
        return self.db.query(self.model).get(obj_id)

    def get_all(self):
        """查询所有"""
        return self.db.query(self.model).all()

    def close(self):
        """手动关闭（可选，程序退出时调用）"""
        self.db.close()