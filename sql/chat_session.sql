-- 如果表已存在则删除
DROP TABLE IF EXISTS chat_session;

-- 创建表
CREATE TABLE chat_session (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    llm_id INTEGER NOT NULL,
    is_new_session SMALLINT NOT NULL DEFAULT 1,
    session_topic VARCHAR(255) DEFAULT NULL,
    created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted SMALLINT DEFAULT 0
);

-- 普通索引
CREATE INDEX idx_user_id ON chat_session (user_id);

-- 表注释
COMMENT ON TABLE chat_session IS '记录用户一次完整对话窗口';

-- 列注释
COMMENT ON COLUMN chat_session.id IS '会话ID(主键)';
COMMENT ON COLUMN chat_session.user_id IS '用户ID';
COMMENT ON COLUMN chat_session.llm_id IS '机器人ID';
COMMENT ON COLUMN chat_session.is_new_session IS '是否为新窗口 1=是 0=不是';
COMMENT ON COLUMN chat_session.session_topic IS '会话主题';
COMMENT ON COLUMN chat_session.created_time IS '创建时间';
COMMENT ON COLUMN chat_session.update_time IS '更新时间';
COMMENT ON COLUMN chat_session.is_deleted IS '软删除';

-- 插入数据（显式指定列名）
INSERT INTO chat_session (
    id, user_id, llm_id, is_new_session, session_topic,
    created_time, update_time, is_deleted
) VALUES
(64, 12, 1, 1, '问候交流', '2026-05-26 17:00:07', '2026-05-26 17:00:08', 0);

-- 重置序列，避免后续插入主键冲突
SELECT setval(
    pg_get_serial_sequence('chat_session', 'id'),
    (SELECT MAX(id) FROM chat_session)
);