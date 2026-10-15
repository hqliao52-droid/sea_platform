/*
 Navicat Premium Dump SQL

 Source Server         : docker-localhost
 Source Server Type    : PostgreSQL
 Source Server Version : 160015 (160015)
 Source Host           : localhost:15433
 Source Catalog        : sea_data
 Source Schema         : platform_center

 Target Server Type    : PostgreSQL
 Target Server Version : 160015 (160015)
 File Encoding         : 65001

 Date: 14/09/2026 15:42:28
*/


-- ----------------------------
-- Table structure for news
-- ----------------------------
DROP TABLE IF EXISTS "platform_center"."news";
CREATE TABLE "platform_center"."news" (
  "id" int4 NOT NULL DEFAULT nextval('news_id_seq'::regclass),
  "category_id" int4 NOT NULL,
  "category_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "title" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "url" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "source" varchar(255) COLLATE "pg_catalog"."default",
  "published_at" timestamp(6),
  "created_at" timestamp(6),
  "is_policy" int4
)
;
COMMENT ON COLUMN "platform_center"."news"."category_id" IS '分类ID';
COMMENT ON COLUMN "platform_center"."news"."category_name" IS '分类名称';
COMMENT ON COLUMN "platform_center"."news"."title" IS '新闻标题';
COMMENT ON COLUMN "platform_center"."news"."url" IS '新闻URL';
COMMENT ON COLUMN "platform_center"."news"."source" IS 'RSS来源';
COMMENT ON COLUMN "platform_center"."news"."published_at" IS '发布时间';
COMMENT ON COLUMN "platform_center"."news"."created_at" IS '创建时间';
COMMENT ON COLUMN "platform_center"."news"."is_policy" IS '是否是政策类';
COMMENT ON TABLE "platform_center"."news" IS '新闻资讯表';

-- ----------------------------
-- Records of news
-- ----------------------------

-- ----------------------------
-- Indexes structure for table news
-- ----------------------------
CREATE INDEX "ix_news_id" ON "platform_center"."news" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table news
-- ----------------------------
ALTER TABLE "platform_center"."news" ADD CONSTRAINT "news_pkey" PRIMARY KEY ("id");
