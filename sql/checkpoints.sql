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

 Date: 14/09/2026 15:49:48
*/


-- ----------------------------
-- Table structure for checkpoints
-- ----------------------------
DROP TABLE IF EXISTS "langgraph"."checkpoints";
CREATE TABLE "langgraph"."checkpoints" (
  "thread_id" text COLLATE "pg_catalog"."default" NOT NULL,
  "checkpoint_ns" text COLLATE "pg_catalog"."default" NOT NULL DEFAULT ''::text,
  "checkpoint_id" text COLLATE "pg_catalog"."default" NOT NULL,
  "parent_checkpoint_id" text COLLATE "pg_catalog"."default",
  "type" text COLLATE "pg_catalog"."default",
  "checkpoint" jsonb NOT NULL,
  "metadata" jsonb NOT NULL DEFAULT '{}'::jsonb
)
;

-- ----------------------------
-- Records of checkpoints
-- ----------------------------

-- ----------------------------
-- Indexes structure for table checkpoints
-- ----------------------------
CREATE INDEX "checkpoints_thread_id_idx" ON "langgraph"."checkpoints" USING btree (
  "thread_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table checkpoints
-- ----------------------------
ALTER TABLE "langgraph"."checkpoints" ADD CONSTRAINT "checkpoints_pkey" PRIMARY KEY ("thread_id", "checkpoint_ns", "checkpoint_id");
