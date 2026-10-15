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

 Date: 15/10/2026 13:59:30
*/


-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS "platform_center"."category";
CREATE TABLE "platform_center"."category" (
  "id" int4 NOT NULL DEFAULT nextval('"platform_center".category_id_seq'::regclass),
  "tag_name" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "is_active" int2 DEFAULT 1,
  "updated_at" timestamp(6),
  "created_at" timestamp(6),
  "example" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying
)
;
COMMENT ON COLUMN "platform_center"."category"."tag_name" IS '类名';
COMMENT ON COLUMN "platform_center"."category"."is_active" IS '启用状态 1：是 0：否';
COMMENT ON COLUMN "platform_center"."category"."updated_at" IS '更新时间';
COMMENT ON COLUMN "platform_center"."category"."created_at" IS '创建时间';
COMMENT ON COLUMN "platform_center"."category"."example" IS '子类别举例，顿号分割。eg:整车出口、海外建厂、充电桩、电池、锂电池、固态电池、回收利用、太阳能板、户用储能、工商业储能、电动摩托、电单车';
COMMENT ON TABLE "platform_center"."category" IS '类别/栏目';

-- ----------------------------
-- Records of category
-- ----------------------------
INSERT INTO "platform_center"."category" VALUES (6, '科技与数字服务', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', 'SaaS、云服务/IDC、AI/大模型、网络安全、金融科技');
INSERT INTO "platform_center"."category" VALUES (7, '消费与零售', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '跨境电商、消费电子、家电、服装/配饰、美妆/个护');
INSERT INTO "platform_center"."category" VALUES (8, '新能源与汽车', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '新能源车、动力电池、光伏/储能、电动两轮/三轮车');
INSERT INTO "platform_center"."category" VALUES (9, '内容与社交', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '短视频/直播、游戏、社交App、短剧/网文');
INSERT INTO "platform_center"."category" VALUES (10, '传统制造升级', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '工业装备、医疗器械、生物医药、建材/家居');
INSERT INTO "platform_center"."category" VALUES (11, '服务与基建', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '物流/供应链、企业服务、教育科技、旅游/酒店');
INSERT INTO "platform_center"."category" VALUES (12, '新兴/特殊赛道', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', 'Web3/区块链、宠物经济、农业科技、环保/ESG');
INSERT INTO "platform_center"."category" VALUES (13, '营销与品牌服务', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '海外营销、品牌服务、营销技术');
INSERT INTO "platform_center"."category" VALUES (14, '合规与政策服务', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '政策合规、法律合规、资质认证');
INSERT INTO "platform_center"."category" VALUES (15, '人才与用工服务', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '跨境用工、人才培育、人力服务');
INSERT INTO "platform_center"."category" VALUES (16, '食品与农业出海', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '食品出口、农产品出海、食品合规');
INSERT INTO "platform_center"."category" VALUES (17, '文化与IP出海', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '文化IP、数字文化、文化服务');
INSERT INTO "platform_center"."category" VALUES (18, '硬件与半导体出海', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '半导体、智能硬件、硬件供应链');
INSERT INTO "platform_center"."category" VALUES (19, '跨境支付与金融配套', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '跨境支付、融资服务、金融配套');
INSERT INTO "platform_center"."category" VALUES (21, '金融领域', 1, '2026-05-13 11:58:00', '2026-05-13 11:57:53', '股票、期货、债券、贵金属等');
INSERT INTO "platform_center"."category" VALUES (22, '其他', 1, '2026-05-15 09:14:19', '2026-04-15 17:47:38', '其他');

-- ----------------------------
-- Primary Key structure for table category
-- ----------------------------
ALTER TABLE "platform_center"."category" ADD CONSTRAINT "category_pkey" PRIMARY KEY ("id");
