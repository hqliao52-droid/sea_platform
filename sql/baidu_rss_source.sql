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

 Date: 14/04/2026 18:17:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for baidu_rss_source
-- ----------------------------
DROP TABLE IF EXISTS `baidu_rss_source`;
CREATE TABLE `baidu_rss_source`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '目标网站名称',
  `url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '目标网站URL',
  `category` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '目录',
  `is_child` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '1' COMMENT '是否为子类rss',
  `is_active` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '1' COMMENT '是否可用 1:可用 0:不可用',
  `is_api_key` tinyint NULL DEFAULT 0 COMMENT '是否需要API秘钥 1：是 0：否',
  `update_rate` int NULL DEFAULT NULL COMMENT '更新频率',
  `hot_rate` double NULL DEFAULT NULL COMMENT '热点率',
  `source_score` double NULL DEFAULT NULL COMMENT '综合分数',
  `created_at` datetime NULL DEFAULT NULL COMMENT '构建时间',
  PRIMARY KEY (`id` DESC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = 'RSS地址——feedparser' ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
