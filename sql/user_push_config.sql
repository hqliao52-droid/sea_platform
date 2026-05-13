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

 Date: 13/05/2026 22:09:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_push_config
-- ----------------------------
DROP TABLE IF EXISTS `user_push_config`;
CREATE TABLE user_push_config (
  id BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',

  user_id BIGINT NOT NULL COMMENT '用户ID',

  max_push_amount INT NOT NULL COMMENT '最大消息推送数量',

  is_enabled TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否开启推送',

  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (id),

  -- 一个用户只能有一条配置
  UNIQUE KEY uk_user_id (user_id),

  -- 常见查询：是否启用
  KEY idx_is_enabled (is_enabled),

  -- 时间排序
  KEY idx_created_at (created_at)
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '用户表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_push_config
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
