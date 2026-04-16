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

 Date: 16/04/2026 18:22:15
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for rss_source
-- ----------------------------
DROP TABLE IF EXISTS `rss_source`;
CREATE TABLE `rss_source`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '目标网站名称',
  `url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '目标网站URL',
  `category` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '目录',
  `is_active` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '1' COMMENT '是否可用 1:可用 0:不可用',
  `is_api_key` tinyint NULL DEFAULT 0 COMMENT '是否需要API秘钥 1：是 0：否',
  `update_rate` int NULL DEFAULT NULL COMMENT '更新频率',
  `hot_rate` double NULL DEFAULT NULL COMMENT '热点率',
  `source_score` double NULL DEFAULT NULL COMMENT '综合分数',
  `created_at` datetime NULL DEFAULT NULL COMMENT '构建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 43 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = 'RSS地址——feedparser' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of rss_source
-- ----------------------------
INSERT INTO `rss_source` VALUES (1, '36氪', 'https://36kr.com/feed', NULL, '1', 0, 5, NULL, NULL, '2026-03-16 10:13:47');
INSERT INTO `rss_source` VALUES (2, 'techcrunch', 'https://techcrunch.com/feed/', NULL, '1', 0, 15, NULL, NULL, '2026-03-16 10:17:05');
INSERT INTO `rss_source` VALUES (3, 'venturebeat', 'https://venturebeat.com/feed/', NULL, '1', 0, 15, NULL, NULL, '2026-03-16 10:17:03');
INSERT INTO `rss_source` VALUES (4, 'BBC', 'http://feeds.bbci.co.uk/news/rss.xml', NULL, '1', 0, 10, NULL, NULL, '2026-03-16 10:17:35');
INSERT INTO `rss_source` VALUES (5, 'reutersagency', 'https://www.reutersagency.com/feed/', NULL, '1', 0, 10, NULL, NULL, '2026-03-16 10:17:52');
INSERT INTO `rss_source` VALUES (6, 'Financial Times', 'https://www.ft.com/rss/home', NULL, '1', 0, 30, NULL, NULL, '2026-03-16 10:18:15');
INSERT INTO `rss_source` VALUES (7, 'Hacker News', 'https://hnrss.org/frontpage', NULL, '1', 0, 15, NULL, NULL, '2026-03-16 10:18:42');
INSERT INTO `rss_source` VALUES (8, '开源中国', 'https://www.oschina.net/news/rss', NULL, '1', 0, 5, NULL, NULL, '2026-03-17 11:28:21');
INSERT INTO `rss_source` VALUES (9, 'V2EX', 'https://www.v2ex.com/feed/tab/hot.xml', NULL, '1', 0, 30, NULL, NULL, '2026-04-14 13:30:42');
INSERT INTO `rss_source` VALUES (10, '中国政府网', 'https://www.gov.cn/jsonTag/tp/rss.xml\n', NULL, '1', 0, 20, NULL, NULL, '2026-04-14 13:31:45');
INSERT INTO `rss_source` VALUES (11, '国家发展改革委', 'https://www.ndrc.gov.cn/xxgk/zcfb/rss.xml', NULL, '1', 0, 30, NULL, NULL, '2026-04-14 13:32:02');
INSERT INTO `rss_source` VALUES (12, '工业和信息化部', 'https://www.miit.gov.cn/RRSdy/index.html\n', NULL, '1', 0, 25, NULL, NULL, '2026-04-14 13:32:24');
INSERT INTO `rss_source` VALUES (13, '商务部（外贸、外资、消费、自贸区）', 'https://www.mofcom.gov.cn/article/xxgk/rss.xml', NULL, '1', 0, 15, NULL, NULL, '2026-04-14 13:32:45');
INSERT INTO `rss_source` VALUES (14, '生态环境部', 'https://www.mee.gov.cn/xxgk/rss.xml', NULL, '1', 0, 20, NULL, NULL, '2026-04-14 13:33:11');
INSERT INTO `rss_source` VALUES (15, '人民网', 'http://politics.people.com.cn/rss/politics.xml', NULL, '1', 0, 10, NULL, NULL, '2026-04-14 13:33:36');
INSERT INTO `rss_source` VALUES (16, '新华网', 'http://www.news.cn/rss/politics.xml', NULL, '1', 0, 15, NULL, NULL, '2026-04-14 13:33:53');
INSERT INTO `rss_source` VALUES (17, '财新网', 'https://www.caixin.com/rss/finance.xml', NULL, '1', 0, 10, NULL, NULL, '2026-04-14 13:34:08');
INSERT INTO `rss_source` VALUES (18, '欧盟委员会(欧盟政策与法规)', 'https://ec.europa.eu/newsroom/rss-list.cfm', NULL, '0', 0, 15, NULL, NULL, '2026-04-14 13:34:30');
INSERT INTO `rss_source` VALUES (19, '英国政府网', 'https://www.gov.uk/government/announcements.atom', NULL, '0', 0, 25, NULL, NULL, '2026-04-14 13:34:50');
INSERT INTO `rss_source` VALUES (20, '国务院新闻办公室', 'https://www.scio.gov.cn/xwfb/rss.xml', NULL, '1', 0, 10, NULL, NULL, '2026-04-14 13:36:10');
INSERT INTO `rss_source` VALUES (21, '司法部', 'https://www.moj.gov.cn/xxgk/rss.xml', NULL, '1', 0, 30, NULL, NULL, '2026-04-14 13:36:30');
INSERT INTO `rss_source` VALUES (22, '财政部', 'https://czt.mof.gov.cn/xxgk/rss.xml', NULL, '1', 0, 30, NULL, NULL, '2026-04-14 13:36:55');
INSERT INTO `rss_source` VALUES (23, '央行 / 金融稳定局（货币政策、金融监管）', 'https://www.pbc.gov.cn/rss/rss.xml', NULL, '1', 0, 25, NULL, NULL, '2026-04-14 13:37:16');
INSERT INTO `rss_source` VALUES (24, '美国白宫(新闻稿)', 'https://www.whitehouse.gov/briefing-room/statements-releases/feed/', NULL, '0', 0, 15, NULL, NULL, '2026-04-14 13:37:31');
INSERT INTO `rss_source` VALUES (25, '世界银行', 'https://www.worldbank.org/en/rss', NULL, '0', 0, 30, NULL, NULL, '2026-04-14 13:37:50');
INSERT INTO `rss_source` VALUES (26, '36氪-快讯', 'https://36kr.com/feed-newsflash', NULL, '1', 0, 5, NULL, NULL, '2026-04-14 16:53:40');
INSERT INTO `rss_source` VALUES (27, '36氪-文章', 'https://36kr.com/feed-article', NULL, '1', 0, 5, NULL, NULL, '2026-04-14 16:54:02');
INSERT INTO `rss_source` VALUES (28, '36氪-动态', 'https://36kr.com/feed-moment', NULL, '0', 0, 5, NULL, NULL, '2026-04-14 16:54:26');
INSERT INTO `rss_source` VALUES (29, '月光博客', 'http://feed.williamlong.info/', NULL, '1', 0, 10, NULL, NULL, '2026-04-14 17:23:24');
INSERT INTO `rss_source` VALUES (30, '网易订阅', 'https://www.163.com/rss', NULL, '1', 0, 10, NULL, NULL, '2026-04-14 17:32:24');
INSERT INTO `rss_source` VALUES (31, '新浪中心', 'http://rss.sina.com.cn/news/china/focus15.xml', NULL, '1', 0, 10, NULL, NULL, '2026-04-14 17:33:36');
INSERT INTO `rss_source` VALUES (32, '港澳焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=gangaotai&tn=rss', NULL, '1', 0, 11, NULL, NULL, '2026-04-15 10:50:55');

SET FOREIGN_KEY_CHECKS = 1;
