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

 Date: 14/09/2026 15:49:30
*/


-- ----------------------------
-- Table structure for checkpoint_blobs
-- ----------------------------
DROP TABLE IF EXISTS "langgraph"."checkpoint_blobs";
CREATE TABLE "langgraph"."checkpoint_blobs" (
  "thread_id" text COLLATE "pg_catalog"."default" NOT NULL,
  "checkpoint_ns" text COLLATE "pg_catalog"."default" NOT NULL DEFAULT ''::text,
  "channel" text COLLATE "pg_catalog"."default" NOT NULL,
  "version" text COLLATE "pg_catalog"."default" NOT NULL,
  "type" text COLLATE "pg_catalog"."default" NOT NULL,
  "blob" bytea
)
;

-- ----------------------------
-- Records of checkpoint_blobs
-- ----------------------------

-- ----------------------------
-- Indexes structure for table checkpoint_blobs
-- ----------------------------
CREATE INDEX "checkpoint_blobs_thread_id_idx" ON "langgraph"."checkpoint_blobs" USING btree (
  "thread_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table checkpoint_blobs
-- ----------------------------
ALTER TABLE "langgraph"."checkpoint_blobs" ADD CONSTRAINT "checkpoint_blobs_pkey" PRIMARY KEY ("thread_id", "checkpoint_ns", "channel", "version");
