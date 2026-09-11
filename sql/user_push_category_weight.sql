-- PostgreSQL 兼容版本

-- 如果表已存在则删除
DROP TABLE IF EXISTS user_push_category_weight;

-- 创建表
CREATE TABLE user_push_category_weight (
    id BIGSERIAL PRIMARY KEY,
    push_config_id BIGINT NOT NULL,
    category_id BIGINT DEFAULT NULL,
    weight DECIMAL(5, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_name VARCHAR(50) DEFAULT NULL,
    updated_at TIMESTAMP NOT NULL,
    CONSTRAINT uk_config_category UNIQUE (push_config_id, category_id),
    CONSTRAINT user_push_category_weight_ibfk_1
        FOREIGN KEY (push_config_id)
        REFERENCES user_push_config (id)
        ON DELETE CASCADE
        ON UPDATE RESTRICT
);

-- 列注释
COMMENT ON COLUMN user_push_category_weight.id IS '主键ID';
COMMENT ON COLUMN user_push_category_weight.push_config_id IS '推送表ID';
COMMENT ON COLUMN user_push_category_weight.category_id IS '分类ID';
COMMENT ON COLUMN user_push_category_weight.weight IS '分类权重';
COMMENT ON COLUMN user_push_category_weight.created_at IS '创建时间';
COMMENT ON COLUMN user_push_category_weight.category_name IS '分类名称';
COMMENT ON COLUMN user_push_category_weight.updated_at IS '修改时间';

-- 插入数据（显式指定列名，避免顺序问题）
INSERT INTO user_push_category_weight (
    id, push_config_id, category_id, weight, created_at, category_name, updated_at
) VALUES
(11, 8, 6, 64.00, '2026-05-21 14:33:11', '科技与数字服务', '2026-05-21 14:33:11'),
(12, 8, 7, 80.00, '2026-05-21 14:33:11', '消费与零售',     '2026-05-21 14:33:11'),
(13, 8, 8, 72.00, '2026-05-21 14:33:11', '新能源与汽车',   '2026-05-21 14:33:11');

-- 重置序列，避免后续插入主键冲突
SELECT setval(
    pg_get_serial_sequence('user_push_category_weight', 'id'),
    (SELECT MAX(id) FROM user_push_category_weight)
);