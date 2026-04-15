from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from app.config.mysql_config import Base

# 声明基类（项目中通常统一放在一个base.py文件中）

class NewsDetail(Base):
    """
    新闻详情表 ORM 模型
    对应数据库表：news_details（建议表名小写+下划线，符合数据库规范）
    """
    __tablename__ = "news_detail"

    # 主键ID
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="主键ID",
        description="主键ID"
    )

    # 父ID（原表标注为父ID，对应news_id）
    news_id = Column(
        Integer,
        nullable=True,
        index=True,  # 建议加索引，提升查询性能
        comment="父ID",
        description="父ID"
    )

    # 栏目/类别-id
    category_id = Column(
        Integer,
        nullable=True,
        comment="栏目/类别-id",
        description="栏目/类别-id"
    )

    # 栏目/类别
    category_name = Column(
        String(255),
        nullable=True,
        comment="栏目/类别",
        description="栏目/类别"
    )

    # 文章标题
    title = Column(
        String(255),
        nullable=True,
        comment="文章标题",
        description="文章标题"
    )

    # 文章作者
    authors = Column(
        String(255),
        comment="文章作者",
        description="文章作者"
    )

    # 正文
    content = Column(
        Text,
        comment="正文",
        description="正文"
    )

    # 文章原始url
    url = Column(
        String(255),
        nullable=True,
        comment="文章原始url",
        description="文章原始url"
    )

    # 访问量（原表类型int，长度255不合理，int类型无长度，修正为标准int）
    watched = Column(
        Integer,
        nullable=True,
        default=0,  # 建议默认值0，避免空值
        comment="访问量",
        description="访问量"
    )

    # 关键词
    keywords = Column(
        String(255),
        comment="关键词",
        description="关键词"
    )

    # AI解析输出（json类型）
    ai_origin_output = Column(
        JSON,
        comment="AI解析输出",
        description="AI解析输出"
    )

    # 内容摘要
    summary = Column(
        Text,
        comment="内容",
        description="内容摘要"
    )

    # 原始entry
    origin_entry = Column(
        String(255),
        comment="原始entry",
        description="原始entry"
    )

    # 全文（longtext类型，对应SQLAlchemy的Text，MySQL会自动映射为longtext）
    in_full_page = Column(
        Text,
        comment="全文",
        description="全文"
    )

    # 发布时间
    publiced_at = Column(
        DateTime,
        comment="发布时间",
        description="发布时间"
    )

    # 创建时间（建议自动赋值）
    created_at = Column(
        DateTime,
        default=datetime.now,
        comment="创建时间",
        description="创建时间"
    )

    # 可选：添加__repr__方法，方便调试打印
    def __repr__(self):
        return f"<NewsDetails(id={self.id}, title='{self.title[:20]}...')>"