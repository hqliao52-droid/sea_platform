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

 Date: 15/10/2026 14:00:13
*/


-- ----------------------------
-- Table structure for system_message
-- ----------------------------
DROP TABLE IF EXISTS "platform_center"."system_message";
CREATE TABLE "platform_center"."system_message" (
  "id" int4 NOT NULL DEFAULT nextval('"platform_center".system_message_id_seq'::regclass),
  "system_message" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "is_actived" int2 DEFAULT 1
)
;
COMMENT ON COLUMN "platform_center"."system_message"."id" IS '主键ID';
COMMENT ON COLUMN "platform_center"."system_message"."system_message" IS '系统消息';
COMMENT ON COLUMN "platform_center"."system_message"."is_actived" IS '是否激活 1=激活 0=失效';
COMMENT ON TABLE "platform_center"."system_message" IS '系统消息表';

-- ----------------------------
-- Records of system_message
-- ----------------------------
INSERT INTO "platform_center"."system_message" VALUES (1, '您好！我是您的出海战略助手。我已经整合了今日最新的东南亚市场资讯，您可以针对特定行业或合规政策向我提问。', 1);
INSERT INTO "platform_center"."system_message" VALUES (2, '今天在忙什么？', 1);
INSERT INTO "platform_center"."system_message" VALUES (3, '我们要从哪里开始呢？', 1);
INSERT INTO "platform_center"."system_message" VALUES (4, '有什么我可以帮助你的呢？', 1);

-- ----------------------------
-- Primary Key structure for table system_message
-- ----------------------------
ALTER TABLE "platform_center"."system_message" ADD CONSTRAINT "system_message_pkey" PRIMARY KEY ("id");
