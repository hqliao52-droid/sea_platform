-- 如果表已存在则删除
DROP TABLE IF EXISTS news;

-- 创建表
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    category_id INTEGER DEFAULT NULL,
    category_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) DEFAULT NULL,
    url VARCHAR(512) NOT NULL,
    source VARCHAR(128) DEFAULT NULL,
    published_at TIMESTAMP DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_policy SMALLINT DEFAULT NULL,
    CONSTRAINT uk_url UNIQUE (url),
    CONSTRAINT uniq_url_time UNIQUE (url, published_at)
);

-- 列注释
COMMENT ON COLUMN news.id IS '主键ID';
COMMENT ON COLUMN news.category_id IS '行业分类';
COMMENT ON COLUMN news.category_name IS '行业分类名称';
COMMENT ON COLUMN news.title IS '标题';
COMMENT ON COLUMN news.url IS '原始链接';
COMMENT ON COLUMN news.source IS 'RSS来源';
COMMENT ON COLUMN news.published_at IS '发布时间';
COMMENT ON COLUMN news.created_at IS '爬虫时间';
COMMENT ON COLUMN news.is_policy IS '是否为政策类文章';

-- 插入数据（显式指定列名）
INSERT INTO news (
    id, category_id, category_name, title, url, source,
    published_at, created_at, is_policy
) VALUES
(3690, 20, '其他',
 '36氪首发 | 清华系光计算芯片企业完成数千万天使轮融资，瞄准全波光计算架构',
 'https://36kr.com/p/3807043342475009?f=rss',
 'https://36kr.com/feed',
 '2026-05-13 09:26:14',
 '2026-05-13 11:56:42',
 0);
-- 重置序列，避免后续插入主键冲突
SELECT setval(
    pg_get_serial_sequence('news', 'id'),
    (SELECT MAX(id) FROM news)
);


