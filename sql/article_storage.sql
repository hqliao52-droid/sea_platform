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

 Date: 16/04/2026 22:51:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for article_storage
-- ----------------------------
DROP TABLE IF EXISTS `article_storage`;
CREATE TABLE `article_storage`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `news_id` int NOT NULL COMMENT '新闻ID',
  `article_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文章名',
  `origin_input` json NULL COMMENT '原始输入',
  `created_at` datetime NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '所有新闻/资讯/文章/帖子的原始数据' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of article_storage
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
