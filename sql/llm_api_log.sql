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

 Date: 15/10/2026 13:59:48
*/


-- ----------------------------
-- Table structure for llm_api_log
-- ----------------------------
DROP TABLE IF EXISTS "platform_center"."llm_api_log";
CREATE TABLE "platform_center"."llm_api_log" (
  "id" int8 NOT NULL DEFAULT nextval('"platform_center".llm_api_log_id_seq'::regclass),
  "message_id" int8 NOT NULL,
  "session_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "model_name" varchar(100) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "temperature" float4,
  "prompt_tokens" int4 DEFAULT 0,
  "completion_tokens" int4 DEFAULT 0,
  "total_tokens" int4 DEFAULT 0,
  "status" int2 DEFAULT 0,
  "error_msg" varchar(1000) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "ip_address" varchar(64) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "user_client" varchar(500) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "sensitive_check_result" int2 DEFAULT 0,
  "created_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of llm_api_log
-- ----------------------------

-- ----------------------------
-- Indexes structure for table llm_api_log
-- ----------------------------
CREATE INDEX "idx_message_id" ON "platform_center"."llm_api_log" USING btree (
  "message_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table llm_api_log
-- ----------------------------
ALTER TABLE "platform_center"."llm_api_log" ADD CONSTRAINT "llm_api_log_pkey" PRIMARY KEY ("id");
