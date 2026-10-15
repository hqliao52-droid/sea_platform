/*
 Navicat Premium Dump SQL

 Source Server         : docker-localhost
 Source Server Type    : PostgreSQL
 Source Server Version : 160015 (160015)
 Source Host           : localhost:15433
 Source Catalog        : sea_data
 Source Schema         : platform_center

 Target Server Type    : PostgreSQL
 Target Server Version : 160015 (160015)
 File Encoding         : 65001

 Date: 14/09/2026 15:56:33
*/


-- ----------------------------
-- Table structure for baidu_rss_source
-- ----------------------------
DROP TABLE IF EXISTS "platform_center"."baidu_rss_source";
CREATE TABLE "platform_center"."baidu_rss_source" (
  "id" int8 NOT NULL DEFAULT nextval('baidu_rss_source_id_seq'::regclass),
  "name" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "url" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "category" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "is_child" int2 DEFAULT 1,
  "parent_id" int2,
  "is_active" int2 DEFAULT 1,
  "is_api_key" int2 DEFAULT 0,
  "update_rate" int8,
  "hot_rate" float8,
  "source_score" float8,
  "created_at" timestamp(6)
)
;
COMMENT ON COLUMN "platform_center"."baidu_rss_source"."id" IS '主键ID';
COMMENT ON COLUMN "platform_center"."baidu_rss_source"."name" IS '目标网站名称';
COMMENT ON COLUMN "platform_center"."baidu_rss_source"."url" IS '目标网站URL';
COMMENT ON COLUMN "plat form_center"."baidu_rss_source"."category" IS '目录';
COMMENT ON COLUMN "platform_center"."baidu_rss_source"."is_child" IS '是否为子类rss';
COMMENT ON COLUMN "platform_center"."baidu_rss_source"."parent_id" IS '父节点ID';
COMMENT ON COLUMN "platform_center"."baidu_rss_source"."is_active" IS '是否可用 1:可用 0:不可用';
COMMENT ON COLUMN "platform_center"."baidu_rss_source"."is_api_key" IS '是否需要API秘钥 1：是 0：否';
COMMENT ON COLUMN "platform_center"."baidu_rss_source"."update_rate" IS '更新频率';
COMMENT ON COLUMN "platform_center"."baidu_rss_source"."hot_rate" IS '热点率';
COMMENT ON COLUMN "platform_center"."baidu_rss_source"."source_score" IS '综合分数';
COMMENT ON COLUMN "platform_center"."baidu_rss_source"."created_at" IS '构建时间';
COMMENT ON TABLE "platform_center"."baidu_rss_source" IS 'RSS地址——feedparser';

-- ----------------------------
-- Records of baidu_rss_source
-- ----------------------------
INSERT INTO "platform_center"."baidu_rss_source" VALUES (72, '国内最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=civilnews&tn=rss', NULL, 0, NULL, NULL, NULL, 28, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (73, '时政要闻最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=shizheng&tn=rss', NULL, 1, NULL, NULL, NULL, 19, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (74, '高层动态最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=gaoceng&tn=rss', NULL, 1, NULL, NULL, NULL, 15, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (75, '人事任免最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=gaoceng&tn=rss', NULL, 1, NULL, NULL, NULL, 22, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (76, '台湾最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=taiwan&tn=rss', NULL, 1, NULL, NULL, NULL, 20, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (77, '历史档案最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=lishi&tn=rss', NULL, 1, NULL, NULL, NULL, 34, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (78, '台湾民生最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=twms&tn=rss', NULL, 1, NULL, NULL, NULL, 27, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (79, '港澳最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=twms&tn=rss', NULL, 1, NULL, NULL, NULL, 18, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (80, '国际最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=internews&tn=rss', NULL, 0, NULL, NULL, NULL, 10, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (81, '环球视野最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=hqsy&tn=rss', NULL, 1, NULL, NULL, NULL, 34, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (82, '国际人物最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=renwu&tn=rss', NULL, 1, NULL, NULL, NULL, 20, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (83, '军事最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=mil&tn=rss', NULL, 0, NULL, NULL, NULL, 22, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (84, '中国军情最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=zhongguojq&tn=rss', NULL, 1, NULL, NULL, NULL, 14, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (85, '台海聚焦最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=taihaijj&tn=rss', NULL, 1, NULL, NULL, NULL, 21, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (86, '国际军情最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=guojijq&tn=rss', NULL, 1, NULL, NULL, NULL, 29, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (87, '财经最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=finannews&tn=rss', NULL, 0, NULL, NULL, NULL, 9, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (88, '股票最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=stock&tn=rss', NULL, 1, NULL, NULL, NULL, 26, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (89, '大盘最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=dapan&tn=rss', NULL, 1, NULL, NULL, NULL, 31, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (90, '个股最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=gegu&tn=rss', NULL, 1, NULL, NULL, NULL, 22, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (91, '新股最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=xingu&tn=rss', NULL, 1, NULL, NULL, NULL, 20, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (92, '权证最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=warrant&tn=rss', NULL, 1, NULL, NULL, NULL, 9, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (93, '理财最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=money&tn=rss', NULL, 1, NULL, NULL, NULL, 22, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (94, '基金最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=fund&tn=rss', NULL, 1, NULL, NULL, NULL, 29, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (95, '银行最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=bank&tn=rss', NULL, 1, NULL, NULL, NULL, 22, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (96, '贵金属最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=nmetal&tn=rss', NULL, 1, NULL, NULL, NULL, 15, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (97, '保险最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=insurance&tn=rss', NULL, 1, NULL, NULL, NULL, 26, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (98, '外汇最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=forex&tn=rss', NULL, 1, NULL, NULL, NULL, 25, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (99, '期货最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=futures&tn=rss', NULL, 1, NULL, NULL, NULL, 21, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (100, '宏观经济最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=hongguan&tn=rss', NULL, 1, NULL, NULL, NULL, 9, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (101, '国内最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=hg_guonei&tn=rss', NULL, 1, NULL, NULL, NULL, 28, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (102, '国际最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=hg_guoji&tn=rss', NULL, 1, NULL, NULL, NULL, 33, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (103, '产业经济最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=chanye&tn=rss', NULL, 1, NULL, NULL, NULL, 19, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (104, '互联网最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=internet&tn=rss', NULL, 0, NULL, NULL, NULL, 25, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (105, '人物动态最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=rwdt&tn=rss', NULL, 1, NULL, NULL, NULL, 34, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (106, '公司动态最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=gsdt&tn=rss', NULL, 1, NULL, NULL, NULL, 29, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (107, '搜索引擎最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=search_engine&tn=rss', NULL, 1, NULL, NULL, NULL, 20, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (108, '电子商务最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=e_commerce&tn=rss', NULL, 1, NULL, NULL, NULL, 34, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (109, '网络游戏最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=online_game&tn=rss', NULL, 1, NULL, NULL, NULL, 10, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (110, '房产最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=housenews&tn=rss', NULL, 0, NULL, NULL, NULL, 24, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (111, '各地动态最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=gddt&tn=rss', NULL, 1, NULL, NULL, NULL, 32, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (112, '政策风向最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=zcfx&tn=rss', NULL, 1, NULL, NULL, NULL, 24, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (113, '市场走势最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=shichangzoushi&tn=rss', NULL, 1, NULL, NULL, NULL, 14, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (114, '家居最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=fitment&tn=rss', NULL, 1, NULL, NULL, NULL, 9, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (115, '汽车最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=autonews&tn=rss', NULL, 0, NULL, NULL, NULL, 7, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (116, '新车最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=autobuy&tn=rss', NULL, 1, NULL, NULL, NULL, 25, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (117, '导购最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=daogou&tn=rss', NULL, 1, NULL, NULL, NULL, 26, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (118, '各地行情最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=hangqing&tn=rss', NULL, 1, NULL, NULL, NULL, 13, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (119, '维修养护最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=weixiu&tn=rss', NULL, 1, NULL, NULL, NULL, 27, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (120, '体育最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=sportnews&tn=rss', NULL, 0, NULL, NULL, NULL, 13, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (121, 'NBA最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=nba&tn=rss', NULL, 1, NULL, NULL, NULL, 15, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (122, '姚明-火箭最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=yaoming&tn=rss', NULL, 1, NULL, NULL, NULL, 12, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (123, '易建联-篮网最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=yijianlian&tn=rss', NULL, 1, NULL, NULL, NULL, 32, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (124, '国际足球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=worldsoccer&tn=rss', NULL, 1, NULL, NULL, NULL, 9, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (125, '英超最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Yingchao&tn=rss', NULL, 1, NULL, NULL, NULL, 14, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (126, '意甲最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Yijia&tn=rss', NULL, 1, NULL, NULL, NULL, 31, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (127, '西甲最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Xijia&tn=rss', NULL, 1, NULL, NULL, NULL, 28, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (128, '足球明星最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Zq_star&tn=rss', NULL, 1, NULL, NULL, NULL, 17, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (129, '曼联最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Manutd&tn=rss', NULL, 1, NULL, NULL, NULL, 22, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (130, '阿森纳最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Arsenal&tn=rss', NULL, 1, NULL, NULL, NULL, 7, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (131, '切尔西最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Chelsea&tn=rss', NULL, 1, NULL, NULL, NULL, 18, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (132, '利物浦最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Liverpool&tn=rss', NULL, 1, NULL, NULL, NULL, 12, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (133, 'AC米兰最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=ACMilan&tn=rss', NULL, 1, NULL, NULL, NULL, 10, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (134, '国际米兰最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=InterMilan&tn=rss', NULL, 1, NULL, NULL, NULL, 17, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (135, '尤文图斯最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Juventus&tn=rss', NULL, 1, NULL, NULL, NULL, 24, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (136, '皇马最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=RealMadrid&tn=rss', NULL, 1, NULL, NULL, NULL, 12, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (137, '巴塞罗那最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Barcelona&tn=rss', NULL, 1, NULL, NULL, NULL, 8, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (138, '拜仁最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Bayen&tn=rss', NULL, 1, NULL, NULL, NULL, 13, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (139, '国内足球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=chinasoccer&tn=rss', NULL, 1, NULL, NULL, NULL, 5, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (140, '男足最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=nanzu&tn=rss', NULL, 1, NULL, NULL, NULL, 31, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (141, '女足最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=nvzu&tn=rss', NULL, 1, NULL, NULL, NULL, 29, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (142, '中超最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=zhongchao&tn=rss', NULL, 1, NULL, NULL, NULL, 33, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (143, '球迷最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=cn_qiumi&tn=rss', NULL, 1, NULL, NULL, NULL, 24, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (144, 'CBA最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=cba&tn=rss', NULL, 1, NULL, NULL, NULL, 31, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (145, '赛事最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=cba_match&tn=rss', NULL, 1, NULL, NULL, NULL, 12, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (146, '综合体育最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=othersports&tn=rss', NULL, 1, NULL, NULL, NULL, 24, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (147, '排球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=volleyball&tn=rss', NULL, 1, NULL, NULL, NULL, 19, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (148, '乒乓球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=table-tennis&tn=rss', NULL, 1, NULL, NULL, NULL, 17, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (149, '羽毛球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=badminton&tn=rss', NULL, 1, NULL, NULL, NULL, 23, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (150, '田径最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Athletics&tn=rss', NULL, 1, NULL, NULL, NULL, 14, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (151, '游泳最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=swimming&tn=rss', NULL, 1, NULL, NULL, NULL, 5, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (152, '体操最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=Gymnastics&tn=rss', NULL, 1, NULL, NULL, NULL, 21, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (153, '网球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=volleyball&tn=rss', NULL, 1, NULL, NULL, NULL, 30, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (154, '赛车最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=F1&tn=rss', NULL, 1, NULL, NULL, NULL, 33, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (155, '拳击最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=boxing&tn=rss', NULL, 1, NULL, NULL, NULL, 10, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (156, '台球最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=billiards&tn=rss', NULL, 1, NULL, NULL, NULL, 9, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (157, '娱乐最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=enternews&tn=rss', NULL, 0, NULL, NULL, NULL, 30, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (158, '明星最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=star&tn=rss', NULL, 1, NULL, NULL, NULL, 17, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (159, '爆料最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=star_chuanwen&pn=1', NULL, 1, NULL, NULL, NULL, 8, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (160, '港台最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=star_gangtai&pn=1', NULL, 1, NULL, NULL, NULL, 16, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (161, '内地最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=star_neidi&pn=1', NULL, 1, NULL, NULL, NULL, 6, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (162, '欧美最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=star_oumei&pn=1', NULL, 1, NULL, NULL, NULL, 8, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (163, '日韩最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=star_rihan&pn=1', NULL, 1, NULL, NULL, NULL, 11, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (164, '电影最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=film&tn=rss', NULL, 1, NULL, NULL, NULL, 35, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (165, '电影花絮最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=film_huaxu&tn=rss', NULL, 1, NULL, NULL, NULL, 35, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (166, '电视最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=tv&tn=rss', NULL, 1, NULL, NULL, NULL, 31, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (167, '剧评最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=tv_jupin&tn=rss', NULL, 1, NULL, NULL, NULL, 23, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (168, '音乐最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=music&tn=rss', NULL, 1, NULL, NULL, NULL, 11, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (169, '综艺最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=zongyi&tn=rss', NULL, 1, NULL, NULL, NULL, 19, NULL, NULL, NULL);
INSERT INTO "platform_center"."baidu_rss_source" VALUES (170, '演出最新（百度源）', 'http://news.baidu.com/n?cmd=4&class=yanchu&tn=rss', NULL, 1, NULL, NULL, NULL, 31, NULL, NULL, NULL);

-- ----------------------------
-- Primary Key structure for table baidu_rss_source
-- ----------------------------
ALTER TABLE "platform_center"."baidu_rss_source" ADD CONSTRAINT "baidu_rss_source_pkey" PRIMARY KEY ("id");
