-- 初始化 platform_center schema
-- 此文件按字母排序优先执行，确保后续建表语句引用的 schema 已存在
CREATE SCHEMA IF NOT EXISTS platform_center;
CREATE SCHEMA IF NOT EXISTS langgraph;