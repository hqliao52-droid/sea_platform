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

 Date: 08/06/2026 15:29:13
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
) ENGINE = InnoDB AUTO_INCREMENT = 65 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '记录用户一次完整对话窗口' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of chat_session
-- ----------------------------
INSERT INTO `chat_session` VALUES (49, 12, 1, 1, '铝塑机器人对股市影响', '2026-05-21 18:17:34', '2026-05-21 18:17:35', 0);
INSERT INTO `chat_session` VALUES (50, 8, 1, 1, '新会话', '2026-05-21 11:58:55', '2026-05-21 11:58:55', 0);
INSERT INTO `chat_session` VALUES (51, 13, 1, 1, '询问文章主要内容', '2026-05-21 15:22:24', '2026-05-21 15:22:24', 0);
INSERT INTO `chat_session` VALUES (52, 13, 1, 1, '询问文章内容', '2026-05-21 15:36:30', '2026-05-21 15:36:31', 0);
INSERT INTO `chat_session` VALUES (53, 12, 1, 1, '询问文章主要内容', '2026-05-26 15:50:03', '2026-05-26 15:50:03', 0);
INSERT INTO `chat_session` VALUES (54, 14, 1, 1, '廖红强信息查询', '2026-05-24 22:00:19', '2026-05-24 22:00:19', 0);
INSERT INTO `chat_session` VALUES (55, 13, 1, 1, '询问文章主要内容', '2026-05-26 15:57:28', '2026-05-26 15:57:28', 0);
INSERT INTO `chat_session` VALUES (56, 12, 1, 1, '询问文章主要内容', '2026-05-26 15:56:56', '2026-05-26 15:56:57', 0);
INSERT INTO `chat_session` VALUES (57, 13, 1, 1, '询问文章主要内容', '2026-05-26 16:22:50', '2026-05-26 16:22:50', 0);
INSERT INTO `chat_session` VALUES (58, 12, 1, 1, '询问文章主要内容', '2026-05-26 16:22:48', '2026-05-26 16:22:49', 0);
INSERT INTO `chat_session` VALUES (59, 15, 1, 1, '询问文章内容', '2026-05-26 16:22:48', '2026-05-26 16:22:49', 0);
INSERT INTO `chat_session` VALUES (60, 16, 1, 1, '新会话', '2026-05-26 16:49:53', '2026-05-26 16:49:53', 0);
INSERT INTO `chat_session` VALUES (61, 17, 1, 1, '问候交流', '2026-05-28 16:13:16', '2026-05-28 16:13:16', 0);
INSERT INTO `chat_session` VALUES (62, 13, 1, 1, '问候交流', '2026-06-02 20:09:01', '2026-06-02 20:09:01', 0);
INSERT INTO `chat_session` VALUES (63, 15, 1, 1, '问候交流', '2026-05-26 17:00:07', '2026-05-26 17:00:08', 0);
INSERT INTO `chat_session` VALUES (64, 12, 1, 1, '问候交流', '2026-05-26 17:00:07', '2026-05-26 17:00:08', 0);

SET FOREIGN_KEY_CHECKS = 1;
