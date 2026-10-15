-- 初始化 platform_center schema
-- 此文件按字母排序优先执行，确保后续建表语句引用的 schema 已存在
CREATE SCHEMA IF NOT EXISTS platform_center;
CREATE SCHEMA IF NOT EXISTS langgraph;
-- 创建所有表依赖的序列（按字母排序）
CREATE SEQUENCE IF NOT EXISTS platform_center.article_storage_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.baidu_rss_source_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.category_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.chat_message_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.chat_session_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.llm_api_log_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.news_detail_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.news_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.rss_source_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.system_message_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.user_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.user_profiles_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.user_push_category_weight_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.user_push_config_id_seq;
CREATE SEQUENCE IF NOT EXISTS platform_center.user_push_notify_channel_id_seq;
