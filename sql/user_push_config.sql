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

 Date: 14/09/2026 15:41:59
*/


-- ----------------------------
-- Table structure for user_push_config
-- ----------------------------
DROP TABLE IF EXISTS "platform_center"."user_push_config";
CREATE TABLE "platform_center"."user_push_config" (
  "id" int4 NOT NULL DEFAULT nextval('user_push_config_id_seq'::regclass),
  "user_id" int4 NOT NULL,
  "max_push_amount" int4 NOT NULL,
  "is_enabled" int2 NOT NULL,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "platform_center"."user_push_config"."id" IS '主键ID';
COMMENT ON COLUMN "platform_center"."user_push_config"."user_id" IS '用户ID';
COMMENT ON COLUMN "platform_center"."user_push_config"."max_push_amount" IS '最大消息推送数量';
COMMENT ON COLUMN "platform_center"."user_push_config"."is_enabled" IS '是否开启推送';
COMMENT ON COLUMN "platform_center"."user_push_config"."created_at" IS '创建时间';
COMMENT ON COLUMN "platform_center"."user_push_config"."updated_at" IS '更新时间';
COMMENT ON TABLE "platform_center"."user_push_config" IS '用户推送配置表';

-- ----------------------------
-- Records of user_push_config
-- ----------------------------

-- ----------------------------
-- Indexes structure for table user_push_config
-- ----------------------------
CREATE INDEX "idx_created_at" ON "platform_center"."user_push_config" USING btree (
  "created_at" "pg_catalog"."timestamp_ops" ASC NULLS LAST
);
CREATE INDEX "idx_is_enabled" ON "platform_center"."user_push_config" USING btree (
  "is_enabled" "pg_catalog"."int2_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table user_push_config
-- ----------------------------
ALTER TABLE "platform_center"."user_push_config" ADD CONSTRAINT "uk_user_push_config_user_id" UNIQUE ("user_id");

-- ----------------------------
-- Primary Key structure for table user_push_config
-- ----------------------------
ALTER TABLE "platform_center"."user_push_config" ADD CONSTRAINT "user_push_config_pkey" PRIMARY KEY ("id");
