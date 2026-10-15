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

 Date: 17/09/2026 14:04:08
*/


-- ----------------------------
-- Table structure for user_profiles
-- ----------------------------
DROP TABLE IF EXISTS "platform_center"."user_profiles";
CREATE TABLE "platform_center"."user_profiles" (
  "id" int4 NOT NULL DEFAULT nextval('user_profiles_id_seq'::regclass),
  "user_id" int4 NOT NULL,
  "metadata" jsonb NOT NULL DEFAULT '{"data": [{"profile": "-", "datetime": "-"}]}'::jsonb,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "platform_center"."user_profiles"."id" IS '主键ID';
COMMENT ON COLUMN "platform_center"."user_profiles"."user_id" IS '用户ID';
COMMENT ON COLUMN "platform_center"."user_profiles"."metadata" IS '用户元数据（画像）';
COMMENT ON COLUMN "platform_center"."user_profiles"."created_at" IS '创建时间';
COMMENT ON TABLE "platform_center"."user_profiles" IS '用户的画像表';

-- ----------------------------
-- Records of user_profiles
-- ----------------------------

-- ----------------------------
-- Indexes structure for table user_profiles
-- ----------------------------
CREATE INDEX "idx_user_profiles_user_id" ON "platform_center"."user_profiles" USING btree (
  "user_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table user_profiles
-- ----------------------------
ALTER TABLE "platform_center"."user_profiles" ADD CONSTRAINT "user_profiles_pkey" PRIMARY KEY ("id");
