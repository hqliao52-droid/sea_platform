/*
 Navicat Premium Dump SQL

 Source Server         : sea_mysql
 Source Server Type    : MySQL
 Source Server Version : 80045 (8.0.45)
 Source Host           : localhost:3307
 Source Schema         : sea_data

 Target Server Type    : MySQL
 Target Server Version : 80045 (8.0.45)
 File Encoding         : 65001

 Date: 16/04/2026 18:21:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '类名',
  `is_active` tinyint NULL DEFAULT 1 COMMENT '启用状态 1：是 0：否',
  `updated_at` datetime NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_at` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `example` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '子类别举例，顿号分割。eg:整车出口、海外建厂、充电桩、电池、锂电池、固态电池、回收利用、太阳能板、户用储能、工商业储能、电动摩托、电单车',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '类别/栏目' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of category
-- ----------------------------
INSERT INTO `category` VALUES (6, '科技与数字服务', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', 'SaaS、云服务/IDC、AI/大模型、网络安全、金融科技');
INSERT INTO `category` VALUES (7, '消费与零售', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '跨境电商、消费电子、家电、服装/配饰、美妆/个护');
INSERT INTO `category` VALUES (8, '新能源与汽车', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '新能源车、动力电池、光伏/储能、电动两轮/三轮车');
INSERT INTO `category` VALUES (9, '内容与社交', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '短视频/直播、游戏、社交App、短剧/网文');
INSERT INTO `category` VALUES (10, '传统制造升级', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '工业装备、医疗器械、生物医药、建材/家居');
INSERT INTO `category` VALUES (11, '服务与基建', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '物流/供应链、企业服务、教育科技、旅游/酒店');
INSERT INTO `category` VALUES (12, '新兴/特殊赛道', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', 'Web3/区块链、宠物经济、农业科技、环保/ESG');
INSERT INTO `category` VALUES (13, '营销与品牌服务', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '海外营销、品牌服务、营销技术');
INSERT INTO `category` VALUES (14, '合规与政策服务', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '政策合规、法律合规、资质认证');
INSERT INTO `category` VALUES (15, '人才与用工服务', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '跨境用工、人才培育、人力服务');
INSERT INTO `category` VALUES (16, '食品与农业出海', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '食品出口、农产品出海、食品合规');
INSERT INTO `category` VALUES (17, '文化与IP出海', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '文化IP、数字文化、文化服务');
INSERT INTO `category` VALUES (18, '硬件与半导体出海', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '半导体、智能硬件、硬件供应链');
INSERT INTO `category` VALUES (19, '跨境支付与金融配套', 1, '2026-04-15 17:30:24', '2026-04-15 17:30:24', '跨境支付、融资服务、金融配套');
INSERT INTO `category` VALUES (20, '其他', 1, '2026-04-15 17:47:30', '2026-04-15 17:47:38', '其他');

SET FOREIGN_KEY_CHECKS = 1;
