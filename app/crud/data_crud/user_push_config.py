"""
user_push_config_crud.py

说明：
    这个 CRUD 负责“整个推送配置聚合”的增删改查。

聚合结构：
    UserPushConfigModel
        ├── channels（通知渠道）
        └── weights（分类权重）

设计原则：
    1. CRUD 层只负责“数据库对象构建与操作”
    2. 不负责 commit() / rollback()
    3. commit / rollback 统一在 Service 层控制事务
    4. 利用 relationship + cascade="all, delete-orphan"
       自动维护子表数据

使用方式：
    Service 层：
        try:
            obj = crud.create(db, schema)
            db.commit()
        except:
            db.rollback()
            raise
"""

from sqlalchemy.orm import Session, selectinload

from app.crud.sea_data_base import BaseCRUD

from app.models.user_push_config import UserPushConfigModel
from app.models.user_push_notify_channel import UserPushNotifyChannelModel
from app.models.user_push_category_weight import UserPushCategoryWeightModel

from app.schemas.user_push_config.user_push_config_schema import (
    UserPushConfigSchema,
)


class UserPushConfigCRUD(BaseCRUD):
    """
    用户推送配置 CRUD
    """

    def __init__(self):
        """
        调用父类初始化，指定当前 CRUD 对应的 ORM Model
        """
        super().__init__(UserPushConfigModel)

    # ==========================================================
    # 查询
    # ==========================================================

    def get_by_user_id(
        self,
        db: Session,
        user_id: int,
    ) -> UserPushConfigModel | None:
        """
        根据 user_id 查询完整配置（含 channels + weights）
        参数:
            db:
                SQLAlchemy Session
            user_id:
                用户 ID
        返回:
            UserPushConfigModel 或 None
        说明:
            使用 selectinload 预加载，避免 N+1 查询问题。
        实际 SQL:
            1. SELECT * FROM user_push_config WHERE user_id = ?
            2. SELECT * FROM user_push_notify_channel WHERE push_config_id IN (...)
            3. SELECT * FROM user_push_category_weight WHERE push_config_id IN (...)
        """
        return (
            db.query(UserPushConfigModel)
            .options(
                selectinload(UserPushConfigModel.channels),
                selectinload(UserPushConfigModel.weights),
            )
            .filter(UserPushConfigModel.user_id == user_id)
            .first()
        )

    def insert(
        self,
        db: Session,
        obj_in: UserPushConfigSchema,
    ) -> UserPushConfigModel:
        """
        创建完整推送配置（主表 + 子表）

        参数:
            obj_in:
                前端传入的 Pydantic Schema

        返回:
            新创建的 ORM 对象

        注意:
            1. 不调用 db.commit()
            2. 不调用 db.rollback()
            3. 仅负责构造 ORM 对象并加入 Session

        原理:
            relationship + cascade 会自动处理子对象插入。
        """

        # 1. 创建主表对象
        config = UserPushConfigModel(
            user_id=obj_in.user_id,
            max_push_amount=obj_in.max_push_amount,
            is_enabled=obj_in.is_enabled,
        )

        # 2. 构造通知渠道子对象
        for channel_schema in obj_in.channels:
            channel = UserPushNotifyChannelModel(
                channel_type=channel_schema.channel_type,
                channel_address=channel_schema.channel_address,
                is_enabled=getattr(channel_schema, "is_enabled", 1),
                priority=getattr(channel_schema, "priority", 1),
            )

            # 加入 relationship 集合
            config.channels.append(channel)

        # 3. 构造分类权重子对象
        for weight_schema in obj_in.weights:
            weight = UserPushCategoryWeightModel(
                category_id=weight_schema.category_id,
                weight=weight_schema.weight,
                category_name=weight_schema.category_name,
            )

            # 加入 relationship 集合
            config.weights.append(weight)

        # 4. 加入 Session
        db.add(config)

        # 5. flush:
        #    立即执行 INSERT，
        #    获取自增主键 config.id，
        #    但事务尚未提交。
        db.flush()

        return config

    def update(
        self,
        db: Session,
        db_obj: UserPushConfigModel,
        obj_in: UserPushConfigSchema,
    ) -> UserPushConfigModel:
        """
        更新完整推送配置（主表 + 子表）

        更新策略:
            1. 更新主表字段
            2. 清空旧 channels
            3. 清空旧 weights
            4. 重建新的 channels
            5. 重建新的 weights

        为什么采用“删旧重建”？
            因为：
                - 数据量很小（通常 < 20 条）
                - 实现简单
                - 不容易出错
                - 维护成本低

        依赖:
            cascade="all, delete-orphan"

        注意:
            不调用 commit()
        """

        # 1. 更新主表字段
        db_obj.max_push_amount = obj_in.max_push_amount
        db_obj.is_enabled = obj_in.is_enabled

        # 2. 清空旧的通知渠道
        #    clear() 后：
        #        relationship 集合被清空
        #
        #    由于 cascade="all, delete-orphan"：
        #        原子对象会自动标记为 DELETE
        db_obj.channels.clear()

        # 3. 重建通知渠道
        for channel_schema in obj_in.channels:
            channel = UserPushNotifyChannelModel(
                channel_type=channel_schema.channel_type,
                channel_address=channel_schema.channel_address,
                is_enabled=getattr(channel_schema, "is_enabled", 1),
                priority=getattr(channel_schema, "priority", 1),
            )

            db_obj.channels.append(channel)

        # 4. 清空旧的分类权重
        db_obj.weights.clear()

        # 5. 重建分类权重
        for weight_schema in obj_in.weights:
            weight = UserPushCategoryWeightModel(
                category_id=weight_schema.category_id,
                weight=weight_schema.weight,
                category_name=weight_schema.category_name,
            )

            db_obj.weights.append(weight)

        # 6. flush:
        #    立即同步到数据库，但不提交事务
        db.flush()

        return db_obj

    # 删除
    def remove(
        self,
        db: Session,
        db_obj: UserPushConfigModel,
    ) -> None:
        """
        删除完整配置

        说明:
            删除主对象即可。

        自动删除来源：
            1. ORM: cascade="all, delete-orphan"
            2. MySQL: FOREIGN KEY ... ON DELETE CASCADE

        注意:
            不调用 commit()
        """
        db.delete(db_obj)
        db.flush()