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

 Date: 08/06/2026 15:30:24
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_push_config
-- ----------------------------
DROP TABLE IF EXISTS `user_push_config`;
CREATE TABLE `user_push_config`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `max_push_amount` int NOT NULL COMMENT '最大消息推送数量',
  `is_enabled` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否开启推送',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_is_enabled`(`is_enabled` ASC) USING BTREE,
  INDEX `idx_created_at`(`created_at` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '用户表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_push_config
-- ----------------------------
INSERT INTO `user_push_config` VALUES (6, 12, 12, 0, '2026-05-21 11:16:53', '2026-05-21 11:16:53');
INSERT INTO `user_push_config` VALUES (8, 13, 13, 1, '2026-05-21 14:17:23', '2026-05-21 14:33:11');

SET FOREIGN_KEY_CHECKS = 1;
