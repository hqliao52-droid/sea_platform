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

 Date: 08/06/2026 15:30:07
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
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '系统用户表(JWT登录专用)' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (8, '廖红强', '$argon2id$v=19$m=65536,t=3,p=4$37sXIgRAyFlr7R0DQMiZEw$MGjzx2F7vVl66VBnCGSR8TN0rUVTPZaYp9kFqOkjXNM', 'qqq', '13265489765', NULL, NULL, NULL, 1, 'user', '2026-05-08 15:39:55', '2026-05-21 11:54:35', NULL, '110.191.203.5');
INSERT INTO `user` VALUES (12, 'admin', '$argon2id$v=19$m=65536,t=3,p=4$JaSUsnZuDeHcG6N0DiFkrA$gQsUuWdnKyYWtCXiq4xsJe6V12cGEBVWy13oTsosKg8', 'admin', NULL, NULL, NULL, 'http://106.52.97.98:8000/attach/images/074382c2ea5a4bf5a21c2d37c9babc87.jpg', 1, 'admin', '2026-05-08 16:20:49', '2026-06-05 10:06:35', '2026-06-05 10:06:35', '171.218.194.66');
INSERT INTO `user` VALUES (13, 'admin2', '$argon2id$v=19$m=65536,t=3,p=4$OofwnhOiFKJ0rlVKybn3vg$Moqh9sSnz1PhlasJN2WsYsFFj0Q8cHjge6bRsaAbD14', '222', NULL, NULL, NULL, 'http://106.52.97.98:8000/attach/images/0092ceddb02f4fbbaff89027d45cbb43.jpg', 1, 'user', '2026-05-09 11:58:04', '2026-06-02 15:08:03', '2026-06-02 15:08:03', '171.218.194.66');
INSERT INTO `user` VALUES (14, '12345678911', '$argon2id$v=19$m=65536,t=3,p=4$/b/3fm+NcS5FSGnN2dv7/w$2GPV3Ui78dTCYY419SXS21uFSAA+1NdHnCYCVeRI3wA', '廖红强', NULL, NULL, NULL, NULL, 1, 'user', '2026-05-24 21:58:39', '2026-05-24 21:58:57', '2026-05-24 21:58:57', '106.83.165.74');
INSERT INTO `user` VALUES (15, 'lhq', '$argon2id$v=19$m=65536,t=3,p=4$GiMkJMR4j/G+13qPsdbaGw$6yizirSDZ2n2pokUGHUf/mD4OTnDGQmYx4oY+QQ4eRM', 'lhq', '13265497822', NULL, NULL, 'http://106.52.97.98:8000/attach/images/d81ff18f8087488080c1ea86c6af32be.jpg', 1, 'user', '2026-05-26 16:17:56', '2026-05-26 18:10:31', '2026-05-26 16:18:04', '222.209.78.243');
INSERT INTO `user` VALUES (16, '17828858621', '$argon2id$v=19$m=65536,t=3,p=4$L8UYg5DyXivlvJdS6l0LYQ$PQSapdNXhdRVTNNnOuRorBdDVO4iU5TYGS422NmbFI4', '三心', '17828858621', NULL, NULL, 'http://106.52.97.98:8000/attach/images/f911e2a3b1a74ce7936ed832594dd5aa.jpg', 1, 'user', '2026-05-26 16:49:39', '2026-05-26 16:49:50', '2026-05-26 16:49:50', '222.209.78.243');
INSERT INTO `user` VALUES (17, 'test11', '$argon2id$v=19$m=65536,t=3,p=4$4FxrTQkhpNQ6x7gXIgRg7A$MRKVsRHtyhMtCEvqY3ZJ00WHZXicS/UHolFzIdPCoeI', '三心2', '17828858621', NULL, NULL, 'http://106.52.97.98:8000/attach/images/e08fd76857c9490cb2df911981fd1d62.jpg', 1, 'user', '2026-05-26 16:50:37', '2026-05-26 16:50:45', '2026-05-26 16:50:45', '222.209.78.243');

SET FOREIGN_KEY_CHECKS = 1;
