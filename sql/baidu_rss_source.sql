DROP TABLE IF EXISTS baidu_rss_source;

CREATE TABLE baidu_rss_source (
    id BIGSERIAL PRIMARY KEY,                     -- 见下方说明：用 BIGSERIAL 替代 int UNSIGNED
    name VARCHAR(255) DEFAULT NULL,
    url VARCHAR(255) DEFAULT NULL,
    category VARCHAR(255) DEFAULT NULL,
    is_child SMALLINT DEFAULT 1,
    parent_id SMALLINT DEFAULT NULL,
    is_active SMALLINT DEFAULT 1,
    is_api_key SMALLINT DEFAULT 0,
    update_rate BIGINT DEFAULT NULL,              -- int UNSIGNED → BIGINT
    hot_rate DOUBLE PRECISION DEFAULT NULL,
    source_score DOUBLE PRECISION DEFAULT NULL,
    created_at TIMESTAMP DEFAULT NULL
);

-- 表注释
COMMENT ON TABLE baidu_rss_source IS 'RSS地址——feedparser';

-- 列注释
COMMENT ON COLUMN baidu_rss_source.id IS '主键ID';
COMMENT ON COLUMN baidu_rss_source.name IS '目标网站名称';
COMMENT ON COLUMN baidu_rss_source.url IS '目标网站URL';
COMMENT ON COLUMN baidu_rss_source.category IS '目录';
COMMENT ON COLUMN baidu_rss_source.is_child IS '是否为子类rss';
COMMENT ON COLUMN baidu_rss_source.parent_id IS '父节点ID';
COMMENT ON COLUMN baidu_rss_source.is_active IS '是否可用 1:可用 0:不可用';
COMMENT ON COLUMN baidu_rss_source.is_api_key IS '是否需要API秘钥 1：是 0：否';
COMMENT ON COLUMN baidu_rss_source.update_rate IS '更新频率';
COMMENT ON COLUMN baidu_rss_source.hot_rate IS '热点率';
COMMENT ON COLUMN baidu_rss_source.source_score IS '综合分数';
COMMENT ON COLUMN baidu_rss_source.created_at IS '构建时间';

-- 表为空，若需要与 MySQL 的 AUTO_INCREMENT = 171 对齐：
SELECT setval(
    pg_get_serial_sequence('baidu_rss_source', 'id'),
    171,
    false    -- 下一次 nextval 返回 171
);