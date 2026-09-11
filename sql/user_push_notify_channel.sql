DROP TABLE IF EXISTS user_push_notify_channel;

-- 创建表
CREATE TABLE user_push_notify_channel (
    id BIGSERIAL PRIMARY KEY,
    push_config_id BIGINT NOT NULL,
    channel_type VARCHAR(50) DEFAULT NULL,
    channel_address VARCHAR(255) DEFAULT NULL,
    is_enabled SMALLINT DEFAULT 1,
    priority INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL,
    CONSTRAINT user_push_notify_channel_ibfk_1
        FOREIGN KEY (push_config_id)
        REFERENCES user_push_config (id)
        ON DELETE CASCADE
        ON UPDATE RESTRICT
);

-- 普通索引
CREATE INDEX idx_push_config_id ON user_push_notify_channel (push_config_id);

-- 列注释
COMMENT ON COLUMN user_push_notify_channel.id IS 'id';
COMMENT ON COLUMN user_push_notify_channel.push_config_id IS '推送配置表ID';
COMMENT ON COLUMN user_push_notify_channel.channel_type IS '通知方式';
COMMENT ON COLUMN user_push_notify_channel.channel_address IS '通知地址';
COMMENT ON COLUMN user_push_notify_channel.is_enabled IS '是否启用';
COMMENT ON COLUMN user_push_notify_channel.priority IS '优先级 1~5  1：最高优先级  5：最低优先级';
COMMENT ON COLUMN user_push_notify_channel.created_at IS '创建时间';
COMMENT ON COLUMN user_push_notify_channel.updated_at IS '更新时间';

-- 插入数据（显式指定列名）
INSERT INTO user_push_notify_channel (
    id, push_config_id, channel_type, channel_address,
    is_enabled, priority, created_at, updated_at
) VALUES
(3, 6, 'email', '2044381298@qq.com', 1, 1, '2026-05-21 11:16:53', '2026-05-21 11:16:53'),
(7, 8, 'email', '3228074924@qq.com', 1, 1, '2026-05-21 14:33:11', '2026-05-21 14:33:11');

-- 重置序列，避免后续插入主键冲突
SELECT setval(
    pg_get_serial_sequence('user_push_notify_channel', 'id'),
    (SELECT MAX(id) FROM user_push_notify_channel)
);