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

 Date: 24/04/2026 18:20:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for llm_api_log
-- ----------------------------
DROP TABLE IF EXISTS `llm_api_log`;
CREATE TABLE `llm_api_log`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL COMMENT '关联消息ID',
  `session_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '会话窗口ID',
  `model_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模型名',
  `temperature` float NULL DEFAULT NULL COMMENT '温度',
  `prompt_tokens` int NULL DEFAULT 0 COMMENT '提示词token消耗',
  `completion_tokens` int NULL DEFAULT 0 COMMENT '生成消息所消耗的token',
  `total_tokens` int NULL DEFAULT 0 COMMENT '总token',
  `status` tinyint NULL DEFAULT 0 COMMENT '消息状态 0=待处理, 1=已完成, 2=处理中, 3=失败（如超时/报错）',
  `error_msg` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '失败消息',
  `ip_address` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户地址',
  `user_client` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户的客户端信息',
  `sensitive_check_result` tinyint NULL DEFAULT 0 COMMENT ' \'敏感词检测结果\'',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_message_id`(`message_id` ASC) USING BTREE,
  INDEX `idx_session_id`(`session_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of llm_api_log
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
