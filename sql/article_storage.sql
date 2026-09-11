-- PostgreSQL 兼容版本

DROP TABLE IF EXISTS article_storage;

CREATE TABLE article_storage (
    id SERIAL PRIMARY KEY,
    news_id INTEGER NOT NULL,
    article_name VARCHAR(255) DEFAULT NULL,
    origin_input JSONB DEFAULT NULL,
    created_at TIMESTAMP DEFAULT NULL
);

-- 表注释
COMMENT ON TABLE article_storage IS '所有新闻/资讯/文章/帖子的原始数据';

-- 列注释
COMMENT ON COLUMN article_storage.id IS '主键ID';
COMMENT ON COLUMN article_storage.news_id IS '新闻ID';
COMMENT ON COLUMN article_storage.article_name IS '文章名';
COMMENT ON COLUMN article_storage.origin_input IS '原始输入';
COMMENT ON COLUMN article_storage.created_at IS '创建时间';

-- 插入数据（origin_input 修正为合法 JSON）
INSERT INTO article_storage (id, news_id, article_name, origin_input, created_at) VALUES
(450, 3690, '36氪首发 | 清华系光计算芯片企业完成数千万天使轮融资，瞄准全波光计算架构',
 '""',
 '2026-05-13 11:56:43');

-- 重置序列
SELECT setval(
    pg_get_serial_sequence('article_storage', 'id'),
    (SELECT MAX(id) FROM article_storage)
);