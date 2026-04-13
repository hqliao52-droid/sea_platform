/*
 Navicat Premium Dump SQL

 Source Server         : sea_platform
 Source Server Type    : MySQL
 Source Server Version : 80045 (8.0.45)
 Source Host           : localhost:3307
 Source Schema         : sea_data

 Target Server Type    : MySQL
 Target Server Version : 80045 (8.0.45)
 File Encoding         : 65001

 Date: 14/04/2026 00:19:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for rss_source
-- ----------------------------
DROP TABLE IF EXISTS `rss_source`;
CREATE TABLE `rss_source`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '目标网站名称',
  `url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '目标网站URL',
  `category` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '目录',
  `is_active` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '1' COMMENT '是否可用 1:可用 0:不可用',
  `is_api_key` tinyint NULL DEFAULT 0 COMMENT '是否需要API秘钥 1：是 0：否',
  `update_rate` int NULL DEFAULT NULL COMMENT '更新频率',
  `hot_rate` double NULL DEFAULT NULL COMMENT '热点率',
  `source_score` double NULL DEFAULT NULL COMMENT '综合分数',
  `created_at` datetime NULL DEFAULT NULL COMMENT '构建时间',
  PRIMARY KEY (`id` DESC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = 'RSS地址——feedparser' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of rss_source
-- ----------------------------
INSERT INTO `rss_source` VALUES (8, '开源中国', 'https://www.oschina.net/news/rss', NULL, '1', 0, 5, NULL, NULL, '2026-03-17 11:28:21');
INSERT INTO `rss_source` VALUES (7, 'Hacker News', 'https://hnrss.org/frontpage', NULL, '1', 0, 10, NULL, NULL, '2026-03-16 10:18:42');
INSERT INTO `rss_source` VALUES (6, 'Financial Times', 'https://www.ft.com/rss/home', NULL, '1', 0, 15, NULL, NULL, '2026-03-16 10:18:15');
INSERT INTO `rss_source` VALUES (5, 'reutersagency', 'https://www.reutersagency.com/feed/', NULL, '1', 0, 30, NULL, NULL, '2026-03-16 10:17:52');
INSERT INTO `rss_source` VALUES (4, 'BBC', 'http://feeds.bbci.co.uk/news/rss.xml', NULL, '1', 0, 30, NULL, NULL, '2026-03-16 10:17:35');
INSERT INTO `rss_source` VALUES (3, 'venturebeat', 'https://venturebeat.com/feed/', NULL, '1', 0, 20, NULL, NULL, '2026-03-16 10:17:03');
INSERT INTO `rss_source` VALUES (2, 'techcrunch', 'https://techcrunch.com/feed/', NULL, '1', 0, 10, NULL, NULL, '2026-03-16 10:17:05');
INSERT INTO `rss_source` VALUES (1, '36氪', 'https://36kr.com/feed', NULL, '1', 0, 5, NULL, NULL, '2026-03-16 10:13:47');

SET FOREIGN_KEY_CHECKS = 1;
