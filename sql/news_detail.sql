-- 如果表已存在则删除
DROP TABLE IF EXISTS news_detail;

-- 创建表
CREATE TABLE news_detail (
    id SERIAL PRIMARY KEY,
    news_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) DEFAULT NULL,
    authors VARCHAR(255) DEFAULT NULL,
    content TEXT DEFAULT NULL,
    url VARCHAR(255) DEFAULT NULL,
    watched INTEGER DEFAULT NULL,
    keywords VARCHAR(255) DEFAULT NULL,
    ai_origin_output JSONB DEFAULT NULL,
    summary TEXT DEFAULT NULL,
    origin_entry JSONB DEFAULT NULL,
    in_full_page TEXT DEFAULT NULL,
    published_at TIMESTAMP DEFAULT NULL,
    created_at TIMESTAMP DEFAULT NULL
);

-- 表注释
COMMENT ON TABLE news_detail IS '文章详情';

-- 列注释
COMMENT ON COLUMN news_detail.id IS 'id';
COMMENT ON COLUMN news_detail.news_id IS '父ID';
COMMENT ON COLUMN news_detail.category_id IS '栏目/类别-id';
COMMENT ON COLUMN news_detail.category_name IS '栏目/类别';
COMMENT ON COLUMN news_detail.title IS '标题';
COMMENT ON COLUMN news_detail.authors IS '文章作者';
COMMENT ON COLUMN news_detail.content IS '正文';
COMMENT ON COLUMN news_detail.url IS '文章原始url';
COMMENT ON COLUMN news_detail.watched IS '访问量';
COMMENT ON COLUMN news_detail.keywords IS '关键词';
COMMENT ON COLUMN news_detail.ai_origin_output IS 'AI解析输出';
COMMENT ON COLUMN news_detail.summary IS '内容';
COMMENT ON COLUMN news_detail.origin_entry IS '原始entry';
COMMENT ON COLUMN news_detail.in_full_page IS '全文';
COMMENT ON COLUMN news_detail.published_at IS '发布时间';
COMMENT ON COLUMN news_detail.created_at IS '创建时间';

SELECT setval(
    pg_get_serial_sequence('news_detail', 'id'),
    179,
    false 
);