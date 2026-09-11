-- PostgreSQL 兼容版本

-- 如果表已存在则删除
DROP TABLE IF EXISTS user_push_config;

-- 创建表
CREATE TABLE user_push_config (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    max_push_amount INTEGER NOT NULL,
    is_enabled SMALLINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_user_id UNIQUE (user_id)
);

-- 普通索引
CREATE INDEX idx_is_enabled ON user_push_config (is_enabled);
CREATE INDEX idx_created_at ON user_push_config (created_at);

-- 表注释
COMMENT ON TABLE user_push_config IS '用户表';

-- 列注释
COMMENT ON COLUMN user_push_config.id IS '主键ID';
COMMENT ON COLUMN user_push_config.user_id IS '用户ID';
COMMENT ON COLUMN user_push_config.max_push_amount IS '最大消息推送数量';
COMMENT ON COLUMN user_push_config.is_enabled IS '是否开启推送';
COMMENT ON COLUMN user_push_config.created_at IS '创建时间';
COMMENT ON COLUMN user_push_config.updated_at IS '更新时间';

-- 插入数据（显式指定列名）
INSERT INTO user_push_config (
    id, user_id, max_push_amount, is_enabled, created_at, updated_at
) VALUES
(6, 12, 12, 0, '2026-05-21 11:16:53', '2026-05-21 11:16:53'),
(8, 13, 13, 1, '2026-05-21 14:17:23', '2026-05-21 14:33:11');

-- 重置序列，避免后续插入主键冲突
SELECT setval(
    pg_get_serial_sequence('user_push_config', 'id'),
    (SELECT MAX(id) FROM user_push_config)
);