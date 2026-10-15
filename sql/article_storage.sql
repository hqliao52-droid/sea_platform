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

 Date: 15/10/2026 13:59:14
*/


-- ----------------------------
-- Table structure for article_storage
-- ----------------------------
DROP TABLE IF EXISTS "platform_center"."article_storage";
CREATE TABLE "platform_center"."article_storage" (
  "id" int4 NOT NULL DEFAULT nextval('"platform_center".article_storage_id_seq'::regclass),
  "news_id" int4 NOT NULL,
  "article_name" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "origin_input" jsonb,
  "created_at" timestamp(6)
)
;
COMMENT ON COLUMN "platform_center"."article_storage"."id" IS '主键ID';
COMMENT ON COLUMN "platform_center"."article_storage"."news_id" IS '新闻ID';
COMMENT ON COLUMN "platform_center"."article_storage"."article_name" IS '文章名';
COMMENT ON COLUMN "platform_center"."article_storage"."origin_input" IS '原始输入';
COMMENT ON COLUMN "platform_center"."article_storage"."created_at" IS '创建时间';
COMMENT ON TABLE "platform_center"."article_storage" IS '所有新闻/资讯/文章/帖子的原始数据';

-- ----------------------------
-- Records of article_storage
-- ----------------------------
INSERT INTO "platform_center"."article_storage" VALUES (450, 3690, '36氪首发 | 清华系光计算芯片企业完成数千万天使轮融资，瞄准全波光计算架构', '""', '2026-05-13 11:56:43');

-- ----------------------------
-- Primary Key structure for table article_storage
-- ----------------------------
ALTER TABLE "platform_center"."article_storage" ADD CONSTRAINT "article_storage_pkey" PRIMARY KEY ("id");
