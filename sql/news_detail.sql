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

 Date: 15/10/2026 14:00:00
*/


-- ----------------------------
-- Table structure for news_detail
-- ----------------------------
DROP TABLE IF EXISTS "platform_center"."news_detail";
CREATE TABLE "platform_center"."news_detail" (
  "id" int4 NOT NULL DEFAULT nextval('"platform_center".news_detail_id_seq'::regclass),
  "news_id" int4,
  "category_id" int4,
  "category_name" varchar(255) COLLATE "pg_catalog"."default",
  "title" varchar(255) COLLATE "pg_catalog"."default",
  "authors" varchar(255) COLLATE "pg_catalog"."default",
  "content" text COLLATE "pg_catalog"."default",
  "url" varchar(255) COLLATE "pg_catalog"."default",
  "watched" int4,
  "keywords" varchar(255) COLLATE "pg_catalog"."default",
  "ai_origin_output" jsonb,
  "summary" text COLLATE "pg_catalog"."default",
  "origin_entry" jsonb,
  "in_full_page" text COLLATE "pg_catalog"."default",
  "published_at" timestamp(6),
  "created_at" timestamp(6)
)
;
COMMENT ON COLUMN "platform_center"."news_detail"."id" IS '主键ID';
COMMENT ON COLUMN "platform_center"."news_detail"."news_id" IS '父ID';
COMMENT ON COLUMN "platform_center"."news_detail"."category_id" IS '栏目/类别-id';
COMMENT ON COLUMN "platform_center"."news_detail"."category_name" IS '栏目/类别';
COMMENT ON COLUMN "platform_center"."news_detail"."title" IS '文章标题';
COMMENT ON COLUMN "platform_center"."news_detail"."authors" IS '文章作者';
COMMENT ON COLUMN "platform_center"."news_detail"."content" IS '正文';
COMMENT ON COLUMN "platform_center"."news_detail"."url" IS '文章原始url';
COMMENT ON COLUMN "platform_center"."news_detail"."watched" IS '访问量';
COMMENT ON COLUMN "platform_center"."news_detail"."keywords" IS '关键词';
COMMENT ON COLUMN "platform_center"."news_detail"."ai_origin_output" IS 'AI解析输出';
COMMENT ON COLUMN "platform_center"."news_detail"."summary" IS '内容';
COMMENT ON COLUMN "platform_center"."news_detail"."origin_entry" IS '原始entry';
COMMENT ON COLUMN "platform_center"."news_detail"."in_full_page" IS '全文';
COMMENT ON COLUMN "platform_center"."news_detail"."published_at" IS '发布时间';
COMMENT ON COLUMN "platform_center"."news_detail"."created_at" IS '创建时间';
COMMENT ON TABLE "platform_center"."news_detail" IS '新闻详情表';

-- ----------------------------
-- Records of news_detail
-- ----------------------------

-- ----------------------------
-- Indexes structure for table news_detail
-- ----------------------------
CREATE INDEX "ix_news_detail_news_id" ON "platform_center"."news_detail" USING btree (
  "news_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table news_detail
-- ----------------------------
ALTER TABLE "platform_center"."news_detail" ADD CONSTRAINT "news_detail_pkey" PRIMARY KEY ("id");
