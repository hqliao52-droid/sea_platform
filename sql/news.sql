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

 Date: 15/04/2026 18:02:26
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for news
-- ----------------------------
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NULL DEFAULT NULL COMMENT '行业分类',
  `category_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '标题',
  `url` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '原始链接',
  `source` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT 'RSS来源',
  `published_at` datetime NULL DEFAULT NULL COMMENT '发布时间',
  `created_at` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '爬虫时间',
  `is_policy` tinyint NULL DEFAULT NULL COMMENT '是否为政策类文章',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_url`(`url` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 811 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of news
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
