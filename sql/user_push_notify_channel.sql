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

 Date: 08/06/2026 15:30:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_push_notify_channel
-- ----------------------------
DROP TABLE IF EXISTS `user_push_notify_channel`;
CREATE TABLE `user_push_notify_channel`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'id',
  `push_config_id` bigint NOT NULL COMMENT '推送配置表ID',
  `channel_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '通知方式',
  `channel_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '通知地址',
  `is_enabled` tinyint(1) NULL DEFAULT 1 COMMENT '是否启用',
  `priority` int NULL DEFAULT 1 COMMENT '优先级 1~5  1：最高优先级  5：最低优先级',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `push_config_id`(`push_config_id` ASC) USING BTREE,
  CONSTRAINT `user_push_notify_channel_ibfk_1` FOREIGN KEY (`push_config_id`) REFERENCES `user_push_config` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_push_notify_channel
-- ----------------------------
INSERT INTO `user_push_notify_channel` VALUES (3, 6, 'email', '2044381298@qq.com', 1, 1, '2026-05-21 11:16:53', '2026-05-21 11:16:53');
INSERT INTO `user_push_notify_channel` VALUES (7, 8, 'email', '3228074924@qq.com', 1, 1, '2026-05-21 14:33:11', '2026-05-21 14:33:11');

SET FOREIGN_KEY_CHECKS = 1;
