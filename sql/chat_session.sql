/*
 Navicat Premium Dump SQL

 Source Server         : 阿里云PG
 Source Server Type    : PostgreSQL
 Source Server Version : 160015 (160015)
 Source Host           : 47.108.169.91:15433
 Source Catalog        : sea_data
 Source Schema         : platform_center

 Target Server Type    : PostgreSQL
 Target Server Version : 160015 (160015)
 File Encoding         : 65001

 Date: 15/10/2026 13:59:42
*/


-- ----------------------------
-- Table structure for chat_session
-- ----------------------------
DROP TABLE IF EXISTS "platform_center"."chat_session";
CREATE TABLE "platform_center"."chat_session" (
  "id" int4 NOT NULL DEFAULT nextval('"platform_center".chat_session_id_seq'::regclass),
  "user_id" int4 NOT NULL,
  "llm_id" int4 NOT NULL,
  "is_new_session" int2 NOT NULL DEFAULT 1,
  "session_topic" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "created_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "thread_id" varchar(64) COLLATE "pg_catalog"."default",
  "is_old_api" bool NOT NULL DEFAULT true
)
;
COMMENT ON COLUMN "platform_center"."chat_session"."id" IS '会话ID(主键)';
COMMENT ON COLUMN "platform_center"."chat_session"."user_id" IS '用户ID';
COMMENT ON COLUMN "platform_center"."chat_session"."llm_id" IS '机器人ID';
COMMENT ON COLUMN "platform_center"."chat_session"."is_new_session" IS '是否为新窗口 1=是 0=不是';
COMMENT ON COLUMN "platform_center"."chat_session"."session_topic" IS '会话主题';
COMMENT ON COLUMN "platform_center"."chat_session"."created_time" IS '创建时间';
COMMENT ON COLUMN "platform_center"."chat_session"."update_time" IS '更新时间';
COMMENT ON COLUMN "platform_center"."chat_session"."is_deleted" IS '软删除';
COMMENT ON COLUMN "platform_center"."chat_session"."thread_id" IS 'checkpoint维护thread_id';
COMMENT ON COLUMN "platform_center"."chat_session"."is_old_api" IS '是否旧api（关联thread_id） false: 否 true: 是';
COMMENT ON TABLE "platform_center"."chat_session" IS '记录用户一次完整对话窗口';

-- ----------------------------
-- Records of chat_session
-- ----------------------------
INSERT INTO "platform_center"."chat_session" VALUES (64, 12, 1, 1, '问候交流', '2026-05-26 17:00:07', '2026-05-26 17:00:08', 0, NULL, 't');

-- ----------------------------
-- Indexes structure for table chat_session
-- ----------------------------
CREATE INDEX "idx_user_id" ON "platform_center"."chat_session" USING btree (
  "user_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table chat_session
-- ----------------------------
ALTER TABLE "platform_center"."chat_session" ADD CONSTRAINT "chat_session_pkey" PRIMARY KEY ("id");
