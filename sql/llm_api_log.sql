-- PostgreSQL 兼容版本

-- 如果表已存在则删除
DROP TABLE IF EXISTS llm_api_log;

-- 创建表
CREATE TABLE llm_api_log (
    id BIGSERIAL PRIMARY KEY,
    message_id BIGINT NOT NULL,
    session_id VARCHAR(64) NOT NULL,
    model_name VARCHAR(100) DEFAULT NULL,
    temperature REAL DEFAULT NULL,
    prompt_tokens INTEGER DEFAULT 0,
    completion_tokens INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    status SMALLINT DEFAULT 0,
    error_msg VARCHAR(1000) DEFAULT NULL,
    ip_address VARCHAR(64) DEFAULT NULL,
    user_client VARCHAR(500) DEFAULT NULL,
    sensitive_check_result SMALLINT DEFAULT 0,
    created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 普通索引
CREATE INDEX idx_message_id ON llm_api_log (message_id);
CREATE INDEX idx_session_id ON llm_api_log (session_id);

-- 列注释
COMMENT ON COLUMN llm_api_log.id IS '主键ID';
COMMENT ON COLUMN llm_api_log.message_id IS '关联消息ID';
COMMENT ON COLUMN llm_api_log.session_id IS '会话窗口ID';
COMMENT ON COLUMN llm_api_log.model_name IS '模型名';
COMMENT ON COLUMN llm_api_log.temperature IS '温度';
COMMENT ON COLUMN llm_api_log.prompt_tokens IS '提示词token消耗';
COMMENT ON COLUMN llm_api_log.completion_tokens IS '生成消息所消耗的token';
COMMENT ON COLUMN llm_api_log.total_tokens IS '总token';
COMMENT ON COLUMN llm_api_log.status IS '消息状态 0=待处理, 1=已完成, 2=处理中, 3=失败（如超时/报错）';
COMMENT ON COLUMN llm_api_log.error_msg IS '失败消息';
COMMENT ON COLUMN llm_api_log.ip_address IS '用户地址';
COMMENT ON COLUMN llm_api_log.user_client IS '用户的客户端信息';
COMMENT ON COLUMN llm_api_log.sensitive_check_result IS '敏感词检测结果';
COMMENT ON COLUMN llm_api_log.created_time IS '创建时间';

-- 表为空，序列从 1 开始即可，无需 setval