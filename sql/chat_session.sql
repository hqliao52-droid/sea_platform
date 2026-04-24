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

 Date: 24/04/2026 18:20:22
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for chat_session
-- ----------------------------
DROP TABLE IF EXISTS `chat_session`;
CREATE TABLE `chat_session`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '会话ID(主键)',
  `user_id` int NOT NULL COMMENT '用户ID',
  `llm_id` int NOT NULL COMMENT '机器人ID',
  `is_new_session` tinyint NOT NULL DEFAULT 1 COMMENT '是否为新窗口 1=是 0=不是',
  `session_topic` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '会话主题',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_deleted` tinyint NULL DEFAULT 0 COMMENT '软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '记录用户一次完整对话窗口' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of chat_session
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
