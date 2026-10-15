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

 Date: 14/09/2026 15:49:36
*/


-- ----------------------------
-- Table structure for checkpoint_migrations
-- ----------------------------
DROP TABLE IF EXISTS "langgraph"."checkpoint_migrations";
CREATE TABLE "langgraph"."checkpoint_migrations" (
  "v" int4 NOT NULL
)
;

-- ----------------------------
-- Records of checkpoint_migrations
-- ----------------------------
INSERT INTO "langgraph"."checkpoint_migrations" VALUES (0);
INSERT INTO "langgraph"."checkpoint_migrations" VALUES (1);
INSERT INTO "langgraph"."checkpoint_migrations" VALUES (2);
INSERT INTO "langgraph"."checkpoint_migrations" VALUES (3);
INSERT INTO "langgraph"."checkpoint_migrations" VALUES (4);
INSERT INTO "langgraph"."checkpoint_migrations" VALUES (5);
INSERT INTO "langgraph"."checkpoint_migrations" VALUES (6);
INSERT INTO "langgraph"."checkpoint_migrations" VALUES (7);
INSERT INTO "langgraph"."checkpoint_migrations" VALUES (8);
INSERT INTO "langgraph"."checkpoint_migrations" VALUES (9);

-- ----------------------------
-- Primary Key structure for table checkpoint_migrations
-- ----------------------------
ALTER TABLE "langgraph"."checkpoint_migrations" ADD CONSTRAINT "checkpoint_migrations_pkey" PRIMARY KEY ("v");
