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

 Date: 30/04/2026 18:14:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for chat_message
-- ----------------------------
DROP TABLE IF EXISTS `chat_message`;
CREATE TABLE `chat_message`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '消息ID',
  `session_id` int NOT NULL COMMENT '会话ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `task_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '任务ID',
  `pre_id` int NULL DEFAULT NULL COMMENT '如果是LLM的回答，就不能置空，并且对应值是回复的消息的ID',
  `role` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色（对应message_type:user assistant system tools）',
  `status` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '消息状态 done/streaming/exception',
  `message_type` tinyint NOT NULL COMMENT '1用户 2机器人 3系统 4工具',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '消息内容',
  `llm_refer_data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '引用资料',
  `llm_refer_data_id` int NULL DEFAULT NULL COMMENT '引用资料ID',
  `user_rating` tinyint NULL DEFAULT 0 COMMENT '用户评分 取值：1-5分或1=点赞, 0=无反馈, -1=点踩',
  `current_user_ip_info` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '当前用户IP信息',
  `user_feedback` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户使用反馈内容（用于后续优化模型或prompt）',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_deleted` tinyint NOT NULL DEFAULT 0 COMMENT '是否删除？ 1=是  0=1',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_session_id`(`session_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 145 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '存储用户 / LLM 的每一条消息内容' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of chat_message
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
