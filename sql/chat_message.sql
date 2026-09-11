/*
 Navicat Premium Dump SQL

 Source Server         : docker-localhost
 Source Server Type    : PostgreSQL
 Source Server Version : 160015 (160015)
 Source Host           : localhost:15432
 Source Catalog        : sea_data
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 160015 (160015)
 File Encoding         : 65001

 Date: 11/09/2026 16:36:33
*/


-- ----------------------------
-- Table structure for chat_message
-- ----------------------------
DROP TABLE IF EXISTS "public"."chat_message";
CREATE TABLE "public"."chat_message" (
  "id" int4 NOT NULL DEFAULT nextval('chat_message_id_seq'::regclass),
  "session_id" int4 NOT NULL,
  "user_id" int4 NOT NULL,
  "task_id" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "pre_id" int4,
  "role" varchar(16) COLLATE "pg_catalog"."default" NOT NULL,
  "status" varchar(25) COLLATE "pg_catalog"."default" NOT NULL,
  "message_type" int2 NOT NULL,
  "content" text COLLATE "pg_catalog"."default" NOT NULL,
  "llm_refer_data" jsonb,
  "llm_refer_data_id" jsonb,
  "user_rating" int2 DEFAULT 0,
  "current_user_ip_info" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "user_feedback" varchar(500) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "created_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 NOT NULL DEFAULT 0
)
;
COMMENT ON COLUMN "public"."chat_message"."id" IS '消息ID';
COMMENT ON COLUMN "public"."chat_message"."session_id" IS '会话ID';
COMMENT ON COLUMN "public"."chat_message"."user_id" IS '用户ID';
COMMENT ON COLUMN "public"."chat_message"."task_id" IS '任务ID';
COMMENT ON COLUMN "public"."chat_message"."pre_id" IS '如果是LLM的回答，就不能置空，并且对应值是回复的消息的ID';
COMMENT ON COLUMN "public"."chat_message"."role" IS '角色（对应message_type:user assistant system tools）';
COMMENT ON COLUMN "public"."chat_message"."status" IS '消息状态 done/streaming/exception';
COMMENT ON COLUMN "public"."chat_message"."message_type" IS '1用户 2机器人 3系统 4工具';
COMMENT ON COLUMN "public"."chat_message"."content" IS '消息内容';
COMMENT ON COLUMN "public"."chat_message"."llm_refer_data" IS '引用资料';
COMMENT ON COLUMN "public"."chat_message"."llm_refer_data_id" IS '引用资料ID';
COMMENT ON COLUMN "public"."chat_message"."user_rating" IS '用户评分 取值：1-5分或1=点赞, 0=无反馈, -1=点踩';
COMMENT ON COLUMN "public"."chat_message"."current_user_ip_info" IS '当前用户IP信息';
COMMENT ON COLUMN "public"."chat_message"."user_feedback" IS '用户使用反馈内容（用于后续优化模型或prompt）';
COMMENT ON COLUMN "public"."chat_message"."created_time" IS '创建时间';
COMMENT ON COLUMN "public"."chat_message"."is_deleted" IS '是否删除？ 1=是  0=否';
COMMENT ON TABLE "public"."chat_message" IS '存储用户 / LLM 的每一条消息内容';

-- ----------------------------
-- Records of chat_message
-- ----------------------------

-- ----------------------------
-- Indexes structure for table chat_message
-- ----------------------------
CREATE INDEX "idx_session_id" ON "public"."chat_message" USING btree (
  "session_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table chat_message
-- ----------------------------
ALTER TABLE "public"."chat_message" ADD CONSTRAINT "chat_message_pkey" PRIMARY KEY ("id");
