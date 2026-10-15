/*
 Navicat Premium Dump SQL

 Source Server         : docker-localhost
 Source Server Type    : PostgreSQL
 Source Server Version : 160015 (160015)
 Source Host           : localhost:15433
 Source Catalog        : sea_data
 Source Schema         : langgraph

 Target Server Type    : PostgreSQL
 Target Server Version : 160015 (160015)
 File Encoding         : 65001

 Date: 14/09/2026 15:49:43
*/


-- ----------------------------
-- Table structure for checkpoint_writes
-- ----------------------------
DROP TABLE IF EXISTS "langgraph"."checkpoint_writes";
CREATE TABLE "langgraph"."checkpoint_writes" (
  "thread_id" text COLLATE "pg_catalog"."default" NOT NULL,
  "checkpoint_ns" text COLLATE "pg_catalog"."default" NOT NULL DEFAULT ''::text,
  "checkpoint_id" text COLLATE "pg_catalog"."default" NOT NULL,
  "task_id" text COLLATE "pg_catalog"."default" NOT NULL,
  "idx" int4 NOT NULL,
  "channel" text COLLATE "pg_catalog"."default" NOT NULL,
  "type" text COLLATE "pg_catalog"."default",
  "blob" bytea NOT NULL,
  "task_path" text COLLATE "pg_catalog"."default" NOT NULL DEFAULT ''::text
)
;

-- ----------------------------
-- Records of checkpoint_writes
-- ----------------------------

-- ----------------------------
-- Indexes structure for table checkpoint_writes
-- ----------------------------
CREATE INDEX "checkpoint_writes_thread_id_idx" ON "langgraph"."checkpoint_writes" USING btree (
  "thread_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table checkpoint_writes
-- ----------------------------
ALTER TABLE "langgraph"."checkpoint_writes" ADD CONSTRAINT "checkpoint_writes_pkey" PRIMARY KEY ("thread_id", "checkpoint_ns", "checkpoint_id", "task_id", "idx");
