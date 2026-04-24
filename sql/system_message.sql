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

 Date: 24/04/2026 18:20:53
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for system_message
-- ----------------------------
DROP TABLE IF EXISTS `system_message`;
CREATE TABLE `system_message`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `system_message` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '系统消息',
  `is_actived` tinyint NULL DEFAULT 1 COMMENT '是否激活 1=激活 0=失效',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '系统消息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_message
-- ----------------------------
INSERT INTO `system_message` VALUES (1, '您好！我是您的出海战略助手。我已经整合了今日最新的东南亚市场资讯，您可以针对特定行业或合规政策向我提问。', 1);
INSERT INTO `system_message` VALUES (2, '今天在忙什么？', 1);
INSERT INTO `system_message` VALUES (3, '我们要从哪里开始呢？', 1);
INSERT INTO `system_message` VALUES (4, '有什么我可以帮助你的呢？', 1);

SET FOREIGN_KEY_CHECKS = 1;
