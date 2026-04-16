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

 Date: 16/04/2026 18:21:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for baidu_rss_source
-- ----------------------------
DROP TABLE IF EXISTS `baidu_rss_source`;
CREATE TABLE `baidu_rss_source`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '目标网站名称',
  `url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '目标网站URL',
  `category` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '目录',
  `is_child` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '是否为子类rss',
  `parent_id` tinyint UNSIGNED NULL DEFAULT NULL COMMENT '父节点ID',
  `is_active` tinyint UNSIGNED NULL DEFAULT 1 COMMENT '是否可用 1:可用 0:不可用',
  `is_api_key` tinyint UNSIGNED NULL DEFAULT 0 COMMENT '是否需要API秘钥 1：是 0：否',
  `update_rate` int UNSIGNED NULL DEFAULT NULL COMMENT '更新频率',
  `hot_rate` double NULL DEFAULT NULL COMMENT '热点率',
  `source_score` double NULL DEFAULT NULL COMMENT '综合分数',
  `created_at` datetime NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '构建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 171 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = 'RSS地址——feedparser' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of baidu_rss_source
-- ----------------------------
INSERT INTO `baidu_rss_source` VALUES (1, '国内焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=civilnews&tn=rss', '', 0, 0, 0, 0, 16, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (2, '台湾焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=taiwan&tn=rss', '', 1, 1, 0, 0, 25, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (3, '港澳焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=gangaotai&tn=rss', '', 1, 1, 0, 0, 28, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (4, '国际焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=internews&tn=rss', '', 0, 0, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (5, '环球视野焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=hqsy&tn=rss', '', 1, 4, 0, 0, 26, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (6, '国际人物焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=renwu&tn=rss', '', 1, 4, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (7, '军事焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=mil&tn=rss', '', 0, 0, 0, 0, 12, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (8, '中国军情焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=zhongguojq&tn=rss', '', 1, 7, 0, 0, 26, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (9, '台海聚焦焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=taihaijj&tn=rss', '', 1, 7, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (10, '国际军情焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=guojijq&tn=rss', '', 1, 7, 0, 0, 28, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (11, '财经焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=finannews&tn=rss', '', 0, 0, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (12, '股票焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=stock&tn=rss', '', 1, 11, 0, 0, 21, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (13, '理财焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=money&tn=rss', '', 1, 11, 0, 0, 25, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (14, '宏观经济焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=hongguan&tn=rss', '', 1, 11, 0, 0, 25, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (15, '产业经济焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=chanye&tn=rss', '', 1, 11, 0, 0, 24, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (16, '互联网焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=internet&tn=rss', '', 0, 0, 0, 0, 10, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (17, '人物动态焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=rwdt&tn=rss', '', 1, 16, 0, 0, 27, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (18, '公司动态焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=gsdt&tn=rss', '', 1, 16, 0, 0, 25, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (19, '搜索引擎焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=search_engine&tn=rss', '', 1, 16, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (20, '电子商务焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=e_commerce&tn=rss', '', 1, 16, 0, 0, 26, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (21, '网络游戏焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=online_game&tn=rss', '', 1, 16, 0, 0, 21, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (22, '房产焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=housenews&tn=rss', '', 0, 0, 0, 0, 14, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (23, '各地动态焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=gddt&tn=rss', '', 1, 22, 0, 0, 22, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (24, '政策风向焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=zcfx&tn=rss', '', 1, 22, 0, 0, 21, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (25, '市场走势焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=shichangzoushi&tn=rss', '', 1, 22, 0, 0, 29, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (26, '家居焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=fitment&tn=rss', '', 1, 22, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (27, '汽车焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=autonews&tn=rss', '', 0, 0, 0, 0, 12, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (28, '新车焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=autobuy&tn=rss', '', 1, 27, 0, 0, 21, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (29, '导购焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=daogou&tn=rss', '', 1, 27, 0, 0, 29, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (30, '各地行情焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=hangqing&tn=rss', '', 1, 27, 0, 0, 28, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (31, '维修养护焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=weixiu&tn=rss', '', 1, 27, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (32, '体育焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=sportnews&tn=rss', '', 0, 0, 0, 0, 17, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (33, 'NBA焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=nba&tn=rss', '', 1, 32, 0, 0, 28, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (34, '国际足球焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=worldsoccer&tn=rss', '', 1, 32, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (35, '国内足球焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=chinasoccer&tn=rss', '', 1, 32, 0, 0, 22, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (36, 'CBA焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=cba&tn=rss', '', 1, 32, 0, 0, 21, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (37, '综合体育焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=othersports&tn=rss', '', 1, 32, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (38, '娱乐焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=enternews&tn=rss', '', 0, 0, 0, 0, 13, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (39, '明星焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=star&tn=rss', '', 1, 38, 0, 0, 27, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (40, '电影焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=film&tn=rss', '', 1, 38, 0, 0, 22, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (41, '电视焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=tv&tn=rss', '', 1, 38, 0, 0, 21, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (42, '音乐焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=music&tn=rss', '', 1, 38, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (43, '综艺焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=zongyi&tn=rss', '', 1, 38, 0, 0, 28, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (44, '演出焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=yanchu&tn=rss', '', 1, 38, 0, 0, 23, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (45, '奖项焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=jiangxiang&tn=rss', '', 1, 38, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (46, '游戏焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=gamenews&tn=rss', '', 0, 0, 0, 0, 10, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (47, '网络游戏焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=netgames&tn=rss', '', 1, 46, 0, 0, 24, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (48, '电视游戏焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=tvgames&tn=rss', '', 1, 46, 0, 0, 26, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (49, '电子竞技焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=dianzijingji&tn=rss', '', 1, 46, 0, 0, 29, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (50, '热门游戏焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=remenyouxi&tn=rss', '', 1, 46, 0, 0, 29, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (51, '魔兽世界焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=WOW&tn=rss', '', 1, 46, 0, 0, 22, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (52, '教育焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=edunews&tn=rss', '', 0, 0, 0, 0, 11, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (53, '考试焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=exams&tn=rss', '', 1, 52, 0, 0, 26, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (54, '留学焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=abroad&tn=rss', '', 1, 52, 0, 0, 26, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (55, '就业焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=jiuye&tn=rss', '', 1, 52, 0, 0, 26, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (56, '女人焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=healthnews&tn=rss', '', 0, 0, 0, 0, 19, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (57, '潮流服饰焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=chaoliufs&tn=rss', '', 1, 56, 0, 0, 22, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (58, '美容护肤焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=meironghf&tn=rss', '', 1, 56, 0, 0, 23, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (59, '减肥健身焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=jianfei&tn=rss', '', 1, 56, 0, 0, 21, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (60, '情感两性焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=qinggan&tn=rss', '', 1, 56, 0, 0, 29, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (61, '健康养生焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=jiankang&tn=rss', '', 1, 56, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (62, '科技焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=technnews&tn=rss', '', 0, 0, 0, 0, 15, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (63, '手机焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=cell&tn=rss', '', 1, 62, 0, 0, 26, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (64, '数码焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=digital&tn=rss', '', 1, 62, 0, 0, 25, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (65, '电脑焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=computer&tn=rss', '', 1, 62, 0, 0, 27, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (66, '科普焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=discovery&tn=rss', '', 1, 62, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (67, '社会焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=socianews&tn=rss', '', 0, 0, 0, 0, 18, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (68, '社会与法焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=shyf&tn=rss', '', 1, 67, 0, 0, 21, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (69, '社会万象焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=shwx&tn=rss', '', 1, 67, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (70, '真情时刻焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=zqsk&tn=rss', '', 1, 67, 0, 0, 29, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (71, '奇闻异事焦点（百度源）', 'http://news.baidu.com/n?cmd=1&class=qwys&tn=rss', '', 1, 67, 0, 0, 22, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (72, '国内最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=civilnews&tn=rss', '', 0, 0, 0, 0, 11, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (73, '时政要闻最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=shizheng&tn=rss', '', 1, 72, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (74, '高层动态最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=gaoceng&tn=rss', '', 2, 73, 0, 0, 38, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (76, '台湾最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=taiwan&tn=rss', '', 1, 72, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (77, '历史档案最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=lishi&tn=rss', '', 2, 76, 0, 0, 38, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (78, '台湾民生最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=twms&tn=rss', '', 2, 76, 0, 0, 37, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (80, '国际最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=internews&tn=rss', '', 0, 0, 0, 0, 15, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (81, '环球视野最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=hqsy&tn=rss', '', 1, 80, 0, 0, 26, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (82, '国际人物最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=renwu&tn=rss', '', 1, 80, 0, 0, 25, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (83, '军事最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=mil&tn=rss', '', 0, 0, 0, 0, 13, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (84, '中国军情最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=zhongguojq&tn=rss', '', 1, 83, 0, 0, 23, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (85, '台海聚焦最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=taihaijj&tn=rss', '', 1, 83, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (86, '国际军情最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=guojijq&tn=rss', '', 1, 83, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (87, '财经最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=finannews&tn=rss', '', 0, 0, 0, 0, 15, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (88, '股票最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=stock&tn=rss', '', 1, 87, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (89, '大盘最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=dapan&tn=rss', '', 2, 88, 0, 0, 38, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (90, '个股最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=gegu&tn=rss', '', 2, 88, 0, 0, 36, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (91, '新股最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=xingu&tn=rss', '', 2, 88, 0, 0, 34, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (92, '权证最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=warrant&tn=rss', '', 2, 88, 0, 0, 32, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (93, '理财最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=money&tn=rss', '', 1, 87, 0, 0, 21, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (94, '基金最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=fund&tn=rss', '', 2, 93, 0, 0, 34, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (95, '银行最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=bank&tn=rss', '', 2, 93, 0, 0, 36, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (96, '贵金属最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=nmetal&tn=rss', '', 2, 93, 0, 0, 32, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (97, '保险最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=insurance&tn=rss', '', 2, 93, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (98, '外汇最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=forex&tn=rss', '', 2, 93, 0, 0, 32, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (99, '期货最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=futures&tn=rss', '', 2, 93, 0, 0, 32, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (100, '宏观经济最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=hongguan&tn=rss', '', 1, 87, 0, 0, 25, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (101, '国内最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=hg_guonei&tn=rss', '', 2, 100, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (102, '国际最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=hg_guoji&tn=rss', '', 2, 100, 0, 0, 37, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (103, '产业经济最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=chanye&tn=rss', '', 1, 87, 0, 0, 24, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (104, '互联网最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=internet&tn=rss', '', 0, 0, 0, 0, 10, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (105, '人物动态最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=rwdt&tn=rss', '', 1, 104, 0, 0, 28, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (106, '公司动态最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=gsdt&tn=rss', '', 1, 104, 0, 0, 26, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (107, '搜索引擎最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=search_engine&tn=rss', '', 1, 104, 0, 0, 23, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (108, '电子商务最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=e_commerce&tn=rss', '', 1, 104, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (109, '网络游戏最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=online_game&tn=rss', '', 1, 104, 0, 0, 27, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (110, '房产最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=housenews&tn=rss', '', 0, 0, 0, 0, 18, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (111, '各地动态最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=gddt&tn=rss', '', 1, 110, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (112, '政策风向最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=zcfx&tn=rss', '', 1, 110, 0, 0, 22, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (113, '市场走势最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=shichangzoushi&tn=rss', '', 1, 110, 0, 0, 21, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (114, '家居最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=fitment&tn=rss', '', 1, 110, 0, 0, 26, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (115, '汽车最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=autonews&tn=rss', '', 0, 0, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (116, '新车最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=autobuy&tn=rss', '', 1, 115, 0, 0, 23, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (117, '导购最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=daogou&tn=rss', '', 1, 115, 0, 0, 27, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (118, '各地行情最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=hangqing&tn=rss', '', 1, 115, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (119, '维修养护最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=weixiu&tn=rss', '', 1, 115, 0, 0, 24, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (120, '体育最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=sportnews&tn=rss', '', 0, 0, 0, 0, 15, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (121, 'NBA最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=nba&tn=rss', '', 1, 120, 0, 0, 26, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (122, '姚明-火箭最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=yaoming&tn=rss', '', 2, 121, 0, 0, 37, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (123, '易建联-篮网最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=yijianlian&tn=rss', '', 2, 121, 0, 0, 37, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (124, '国际足球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=worldsoccer&tn=rss', '', 1, 120, 0, 0, 28, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (125, '英超最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Yingchao&tn=rss', '', 2, 124, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (126, '意甲最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Yijia&tn=rss', '', 2, 124, 0, 0, 39, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (127, '西甲最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Xijia&tn=rss', '', 2, 124, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (128, '足球明星最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Zq_star&tn=rss', '', 2, 124, 0, 0, 38, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (129, '曼联最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Manutd&tn=rss', '', 2, 124, 0, 0, 32, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (130, '阿森纳最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Arsenal&tn=rss', '', 2, 124, 0, 0, 38, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (131, '切尔西最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Chelsea&tn=rss', '', 2, 124, 0, 0, 40, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (132, '利物浦最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Liverpool&tn=rss', '', 2, 124, 0, 0, 39, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (133, 'AC米兰最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=ACMilan&tn=rss', '', 2, 124, 0, 0, 37, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (134, '国际米兰最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=InterMilan&tn=rss', '', 2, 124, 0, 0, 34, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (135, '尤文图斯最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Juventus&tn=rss', '', 2, 124, 0, 0, 37, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (136, '皇马最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=RealMadrid&tn=rss', '', 2, 124, 0, 0, 39, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (137, '巴塞罗那最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Barcelona&tn=rss', '', 2, 124, 0, 0, 32, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (138, '拜仁最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Bayen&tn=rss', '', 2, 124, 0, 0, 38, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (139, '国内足球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=chinasoccer&tn=rss', '', 1, 120, 0, 0, 22, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (140, '男足最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=nanzu&tn=rss', '', 2, 139, 0, 0, 32, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (141, '女足最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=nvzu&tn=rss', '', 2, 139, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (142, '中超最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=zhongchao&tn=rss', '', 2, 139, 0, 0, 31, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (143, '球迷最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=cn_qiumi&tn=rss', '', 2, 139, 0, 0, 39, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (144, 'CBA最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=cba&tn=rss', '', 1, 120, 0, 0, 22, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (145, '赛事最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=cba_match&tn=rss', '', 2, 144, 0, 0, 36, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (146, '综合体育最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=othersports&tn=rss', '', 1, 120, 0, 0, 27, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (147, '排球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=volleyball&tn=rss', '', 2, 146, 0, 0, 34, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (148, '乒乓球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=table-tennis&tn=rss', '', 2, 146, 0, 0, 33, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (149, '羽毛球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=badminton&tn=rss', '', 2, 146, 0, 0, 38, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (150, '田径最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Athletics&tn=rss', '', 2, 146, 0, 0, 34, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (151, '游泳最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=swimming&tn=rss', '', 2, 146, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (152, '体操最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Gymnastics&tn=rss', '', 2, 146, 0, 0, 39, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (154, '赛车最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=F1&tn=rss', '', 2, 146, 0, 0, 33, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (155, '拳击最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=boxing&tn=rss', '', 2, 146, 0, 0, 36, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (156, '台球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=billiards&tn=rss', '', 2, 146, 0, 0, 38, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (157, '娱乐最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=enternews&tn=rss', '', 0, 0, 0, 0, 15, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (158, '明星最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=star&tn=rss', '', 1, 157, 0, 0, 25, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (159, '爆料最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=star_chuanwen&pn=1', '', 2, 158, 0, 0, 36, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (160, '港台最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=star_gangtai&pn=1', '', 2, 158, 0, 0, 34, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (161, '内地最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=star_neidi&pn=1', '', 2, 158, 0, 0, 39, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (162, '欧美最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=star_oumei&pn=1', '', 2, 158, 0, 0, 38, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (163, '日韩最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=star_rihan&pn=1', '', 2, 158, 0, 0, 40, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (164, '电影最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=film&tn=rss', '', 1, 157, 0, 0, 24, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (165, '电影花絮最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=film_huaxu&tn=rss', '', 2, 164, 0, 0, 34, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (166, '电视最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=tv&tn=rss', '', 1, 157, 0, 0, 20, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (167, '剧评最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=tv_jupin&tn=rss', '', 2, 166, 0, 0, 40, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (168, '音乐最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=music&tn=rss', '', 1, 157, 0, 0, 30, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (169, '综艺最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=zongyi&tn=rss', '', 1, 157, 0, 0, 28, 0, 0, '2026-04-15 10:47:18');
INSERT INTO `baidu_rss_source` VALUES (170, '演出最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=yanchu&tn=rss', '', 1, 157, 0, 0, 24, 0, 0, '2026-04-15 10:47:18');

SET FOREIGN_KEY_CHECKS = 1;
