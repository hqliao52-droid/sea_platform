/*
 Navicat Premium Dump SQL

 Source Server         : docker-localhost
 Source Server Type    : PostgreSQL
 Source Server Version : 160015 (160015)
 Source Host           : localhost:15432
 Source Catalog        : sea_data
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 160015 (160015)
 File Encoding         : 65001

 Date: 11/09/2026 16:44:51
*/


-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "public"."user";
CREATE TABLE "public"."user" (
  "id" int8 NOT NULL DEFAULT nextval('user_id_seq'::regclass),
  "username" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "password" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "nickname" varchar(50) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "phone" varchar(20) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "email" varchar(100) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "city" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "avatar" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "status" int2 NOT NULL DEFAULT 1,
  "role" varchar(20) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'user'::character varying,
  "created_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "last_login_time" timestamp(6),
  "last_login_ip" varchar(50) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying
)
;
COMMENT ON COLUMN "public"."user"."id" IS '用户唯一ID(主键)';
COMMENT ON COLUMN "public"."user"."username" IS '登录账号(唯一)';
COMMENT ON COLUMN "public"."user"."password" IS '加密后的密码(BCrypt)';
COMMENT ON COLUMN "public"."user"."nickname" IS '昵称';
COMMENT ON COLUMN "public"."user"."phone" IS '手机号';
COMMENT ON COLUMN "public"."user"."email" IS '邮箱';
COMMENT ON COLUMN "public"."user"."city" IS '所在城市';
COMMENT ON COLUMN "public"."user"."avatar" IS '头像URL';
COMMENT ON COLUMN "public"."user"."status" IS '用户状态 1-正常 0-禁用 2-锁定';
COMMENT ON COLUMN "public"."user"."role" IS '角色 user/admin';
COMMENT ON COLUMN "public"."user"."created_time" IS '创建时间';
COMMENT ON COLUMN "public"."user"."updated_time" IS '更新时间';
COMMENT ON COLUMN "public"."user"."last_login_time" IS '最后登录时间';
COMMENT ON COLUMN "public"."user"."last_login_ip" IS '最后登录IP';
COMMENT ON TABLE "public"."user" IS '系统用户表(JWT登录专用)';

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO "public"."user" VALUES (1, 'admin', '$argon2id$v=19$m=65536,t=3,p=4$bY2RUso5p/S+F6KUEuI8Zw$TASu1ww8kd+Yv9rezpHjpdQD5HlWyzughkYzakorWDU', 'qqq', '133333333333', NULL, NULL, NULL, 1, 'admin', '2026-05-08 15:39:55', '2026-09-11 16:40:17.992991', '2026-09-11 16:40:17.989787', '172.19.0.1');

-- ----------------------------
-- Uniques structure for table user
-- ----------------------------
ALTER TABLE "public"."user" ADD CONSTRAINT "uk_username" UNIQUE ("username");

-- ----------------------------
-- Primary Key structure for table user
-- ----------------------------
ALTER TABLE "public"."user" ADD CONSTRAINT "user_pkey" PRIMARY KEY ("id");
