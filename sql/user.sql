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

 Date: 30/04/2026 18:15:18
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '用户唯一ID(主键)',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录账号(唯一)',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '加密后的密码(BCrypt)',
  `nickname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '昵称',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱',
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '所在城市',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '头像URL',
  `status` tinyint NOT NULL DEFAULT 1 COMMENT '用户状态 1-正常 0-禁用 2-锁定',
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'user' COMMENT '角色 user/admin',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `last_login_time` datetime NULL DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '最后登录IP',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_username`(`username` ASC) USING BTREE COMMENT '账号唯一索引'
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '系统用户表(JWT登录专用)' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
