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

 Date: 15/10/2026 14:00:45
*/


-- ----------------------------
-- Table structure for user_push_notify_channel
-- ----------------------------
DROP TABLE IF EXISTS "platform_center"."user_push_notify_channel";
CREATE TABLE "platform_center"."user_push_notify_channel" (
  "id" int4 NOT NULL DEFAULT nextval('"platform_center".user_push_notify_channel_id_seq'::regclass),
  "push_config_id" int4 NOT NULL,
  "channel_type" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "channel_address" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "is_enabled" int2 NOT NULL,
  "priority" int4 NOT NULL,
  "created_at" timestamp(6),
  "updated_at" timestamp(6)
)
;
COMMENT ON COLUMN "platform_center"."user_push_notify_channel"."id" IS 'id';
COMMENT ON COLUMN "platform_center"."user_push_notify_channel"."push_config_id" IS '推送配置表ID';
COMMENT ON COLUMN "platform_center"."user_push_notify_channel"."channel_type" IS '通知方式';
COMMENT ON COLUMN "platform_center"."user_push_notify_channel"."channel_address" IS '通知地址';
COMMENT ON COLUMN "platform_center"."user_push_notify_channel"."is_enabled" IS '是否启用';
COMMENT ON COLUMN "platform_center"."user_push_notify_channel"."priority" IS '优先级 1~5  1：最高优先级  5：最低优先级';
COMMENT ON COLUMN "platform_center"."user_push_notify_channel"."created_at" IS '创建时间';
COMMENT ON COLUMN "platform_center"."user_push_notify_channel"."updated_at" IS '修改时间';
COMMENT ON TABLE "platform_center"."user_push_notify_channel" IS '用户推送通知渠道表';

-- ----------------------------
-- Records of user_push_notify_channel
-- ----------------------------

-- ----------------------------
-- Indexes structure for table user_push_notify_channel
-- ----------------------------
CREATE INDEX "push_config_id" ON "platform_center"."user_push_notify_channel" USING btree (
  "push_config_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table user_push_notify_channel
-- ----------------------------
ALTER TABLE "platform_center"."user_push_notify_channel" ADD CONSTRAINT "uk_channel_type" UNIQUE ("push_config_id", "channel_type");

-- ----------------------------
-- Primary Key structure for table user_push_notify_channel
-- ----------------------------
ALTER TABLE "platform_center"."user_push_notify_channel" ADD CONSTRAINT "user_push_notify_channel_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table user_push_notify_channel
-- ----------------------------
ALTER TABLE "platform_center"."user_push_notify_channel" ADD CONSTRAINT "user_push_notify_channel_push_config_id_fkey" FOREIGN KEY ("push_config_id") REFERENCES "platform_center"."user_push_config" ("id") ON DELETE CASCADE ON UPDATE RESTRICT;
