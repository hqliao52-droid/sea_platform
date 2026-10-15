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

 Date: 14/09/2026 15:42:05
*/


-- ----------------------------
-- Table structure for user_push_category_weight
-- ----------------------------
DROP TABLE IF EXISTS "platform_center"."user_push_category_weight";
CREATE TABLE "platform_center"."user_push_category_weight" (
  "id" int4 NOT NULL DEFAULT nextval('user_push_category_weight_id_seq'::regclass),
  "push_config_id" int4 NOT NULL,
  "category_id" int4 NOT NULL,
  "category_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "weight" numeric(5,2) NOT NULL,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "platform_center"."user_push_category_weight"."id" IS '主键ID';
COMMENT ON COLUMN "platform_center"."user_push_category_weight"."push_config_id" IS '推送表ID';
COMMENT ON COLUMN "platform_center"."user_push_category_weight"."category_id" IS '分类ID';
COMMENT ON COLUMN "platform_center"."user_push_category_weight"."category_name" IS '分类名称';
COMMENT ON COLUMN "platform_center"."user_push_category_weight"."weight" IS '分类权重';
COMMENT ON COLUMN "platform_center"."user_push_category_weight"."created_at" IS '创建时间';
COMMENT ON COLUMN "platform_center"."user_push_category_weight"."updated_at" IS '修改时间';
COMMENT ON TABLE "platform_center"."user_push_category_weight" IS '用户推送分类权重表';

-- ----------------------------
-- Records of user_push_category_weight
-- ----------------------------

-- ----------------------------
-- Uniques structure for table user_push_category_weight
-- ----------------------------
ALTER TABLE "platform_center"."user_push_category_weight" ADD CONSTRAINT "uk_config_category" UNIQUE ("push_config_id", "category_id");

-- ----------------------------
-- Primary Key structure for table user_push_category_weight
-- ----------------------------
ALTER TABLE "platform_center"."user_push_category_weight" ADD CONSTRAINT "user_push_category_weight_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table user_push_category_weight
-- ----------------------------
ALTER TABLE "platform_center"."user_push_category_weight" ADD CONSTRAINT "user_push_category_weight_push_config_id_fkey" FOREIGN KEY ("push_config_id") REFERENCES "platform_center"."user_push_config" ("id") ON DELETE CASCADE ON UPDATE RESTRICT;
