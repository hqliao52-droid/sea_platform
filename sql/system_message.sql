-- PostgreSQL 兼容版本

-- 如果表已存在则删除
DROP TABLE IF EXISTS system_message;

-- 创建表
CREATE TABLE system_message (
    id SERIAL PRIMARY KEY,
    system_message VARCHAR(255) DEFAULT NULL,
    is_actived SMALLINT DEFAULT 1
);

-- 表注释
COMMENT ON TABLE system_message IS '系统消息表';

-- 列注释
COMMENT ON COLUMN system_message.id IS '主键ID';
COMMENT ON COLUMN system_message.system_message IS '系统消息';
COMMENT ON COLUMN system_message.is_actived IS '是否激活 1=激活 0=失效';

-- 插入数据（显式指定列名）
INSERT INTO system_message (id, system_message, is_actived) VALUES
(1, '您好！我是您的出海战略助手。我已经整合了今日最新的东南亚市场资讯，您可以针对特定行业或合规政策向我提问。', 1),
(2, '今天在忙什么？', 1),
(3, '我们要从哪里开始呢？', 1),
(4, '有什么我可以帮助你的呢？', 1);

-- 重置序列，避免后续插入主键冲突
SELECT setval(
    pg_get_serial_sequence('system_message', 'id'),
    (SELECT MAX(id) FROM system_message)
);