/*
 Navicat Premium Dump SQL

 Source Server         : sea_platform
 Source Server Type    : MySQL
 Source Server Version : 80046 (8.0.46)
 Source Host           : 106.52.97.98:3306
 Source Schema         : sea_data

 Target Server Type    : MySQL
 Target Server Version : 80046 (8.0.46)
 File Encoding         : 65001

 Date: 13/05/2026 22:08:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_push_category_weight
-- ----------------------------
DROP TABLE IF EXISTS `user_push_category_weight`;
CREATE TABLE `user_push_category_weight`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `push_config_id` bigint NOT NULL COMMENT '推送表ID',
  `category_id` bigint NOT NULL COMMENT '分类ID',
  `weight` decimal(5, 2) NOT NULL DEFAULT 0.00 COMMENT '分类权重',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_config_category`(`push_config_id` ASC, `category_id` ASC) USING BTREE,
  CONSTRAINT `user_push_category_weight_ibfk_1` FOREIGN KEY (`push_config_id`) REFERENCES `user_push_config` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_push_category_weight
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
