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

 Date: 08/06/2026 15:30:15
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
  `category_id` bigint NULL DEFAULT NULL COMMENT '分类ID',
  `weight` decimal(5, 2) NULL DEFAULT 0.00 COMMENT '分类权重',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `category_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '分类名称',
  `updated_at` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_config_category`(`push_config_id` ASC, `category_id` ASC) USING BTREE,
  CONSTRAINT `user_push_category_weight_ibfk_1` FOREIGN KEY (`push_config_id`) REFERENCES `user_push_config` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_push_category_weight
-- ----------------------------
INSERT INTO `user_push_category_weight` VALUES (11, 8, 6, 64.00, '2026-05-21 14:33:11', '科技与数字服务', '2026-05-21 14:33:11');
INSERT INTO `user_push_category_weight` VALUES (12, 8, 7, 80.00, '2026-05-21 14:33:11', '消费与零售', '2026-05-21 14:33:11');
INSERT INTO `user_push_category_weight` VALUES (13, 8, 8, 72.00, '2026-05-21 14:33:11', '新能源与汽车', '2026-05-21 14:33:11');

SET FOREIGN_KEY_CHECKS = 1;
