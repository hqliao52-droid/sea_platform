## 项目名称：基于 langchain 框架下的新闻消息处理助手
### 一、核心需求（Demend Analysis）：
    利用 AI 能力帮助服务企业出海的机构降低公众号内容运营成本，并提升信息服务能力。
### 二、目标解决（Project）：
    企业出海信息分散且获取效率低，同时公众号运营成本高，因此需要一个基于AI的信息处理平台，自动聚合、分析和生成出海相关内容，为企业提供高效的信息服务。
### 三、服务对象（Object）：
    公众号运营团队、内陆有出海需求、新闻消息订阅的机构/企业/C端用户等
### 四、核心模块（Model）:
    1、信息采取
        数据来源：行业公众号、政策网、出海资讯网站、各企业案例、新闻……
    2、AI内容处理
        利用AI 对信息自动完成：文章总结、topic聚类、keywords提炼、行业分类、政策识别……输出结构化的信息供以阅读/处理。
    3、内容生成与运营
        消息气泡：利用AI 对资讯自动生成类似《今日XXX企业出海咨询》----XXX代指服务端（一对一）
    4、企业服务信息分发
        企业登录账号后，可以使用今日出海资讯、AI问答、个性化内容推送……

目录架构：
```text
sea_ai_platform
├── Qdrant_data_dev     # Qdrant数据集合，个人demo直接放在项目中即可
│   ├── aliases
│   │   └── data.json
│   ├── collections
│   └── raft_state.json
├── README.md
├── app                     # FastAPI项目入口
│   ├── api                    # API 路由模块
│   │   ├── __init__.py
│   │   ├── catrgory_api.py
│   │   ├── chat_message_api.py
│   │   ├── chat_session_api.py
│   │   ├── email_api.py
│   │   ├── file_api.py
│   │   ├── llm_api.py
│   │   ├── news_api.py
│   │   ├── news_detail_api.py
│   │   ├── rss_api.py
│   │   ├── user_api.py
│   │   └── user_config_api.py
│   ├── config                # 配置
│   │   ├── __init__.py
│   │   ├── file_config.py
│   │   ├── llm_config.py
│   │   ├── mysql_config.py
│   │   ├── qdrant_config.py
│   │   ├── rabbitMq_config.py
│   │   ├── redis_config.py
│   │   └── settings.py
│   ├── core                  # core
│   │   ├── scheduler.py        # 定时任务全局配置
│   │   └── user_deps.py        # JWT- token 验证（get_current_user）
│   ├── crawler                # 信息采集
│   │   ├── __init__.py
│   │   ├── news_spider.py
│   │   └── rss_spider.py
│   ├── crud                  # 数据库的操作
│   │   ├── __init__.py
│   │   ├── data_crud           # 数据操作（继承基类）
│   │   │   ├── aricle_storage.py
│   │   │   ├── baidu_rss_source.py
│   │   │   ├── category.py
│   │   │   ├── chat_message.py
│   │   │   ├── chat_session.py
│   │   │   ├── llm_api_log.py
│   │   │   ├── news.py
│   │   │   ├── news_detail.py
│   │   │   ├── rss.py
│   │   │   ├── user.py
│   │   │   └── user_push_config.py
│   │   └── sea_data_base.py        # CRUD 基类
│   ├── main.py                     # FastAPI路由挂载入口
│   ├── models                        # 数据模型（sqlalchemy）
│   │   ├── __init__.py
│   │   ├── article_storage.py
│   │   ├── baidu_rss_source.py
│   │   ├── category.py
│   │   ├── chat_message.py
│   │   ├── chat_session.py
│   │   ├── llm_api_log.py
│   │   ├── news_details_model.py
│   │   ├── news_model.py
│   │   ├── policy_model.py
│   │   ├── rss_source.py
│   │   ├── system_message.py
│   │   ├── user.py
│   │   ├── user_model.py
│   │   ├── user_push_category_weight.py
│   │   ├── user_push_config.py
│   │   └── user_push_notify_channel.py
│   ├── prompt                          # LLM提示词
│   │   └── agent_prompt.py
│   ├── schemas                         # 数据模型（pydantic）
│   │   ├── __init__.py
│   │   ├── agent_orchestrator
│   │   │   └── agent_orchestrator.py
│   │   ├── article_storage
│   │   │   └── article_stoage.py
│   │   ├── baidu_rss_source
│   │   │   └── baidu_rss_source.py
│   │   ├── category
│   │   │   └── category.py
│   │   ├── chat_message
│   │   │   └── chat_message.py
│   │   ├── chat_session
│   │   │   └── chat_session.py
│   │   ├── email_SMTP
│   │   │   └── email_smtp_schema.py
│   │   ├── file
│   │   │   └── file_schema.py
│   │   ├── llm_api_log.py
│   │   │   └── llm_api_log.py
│   │   ├── news
│   │   │   ├── new_schema.py
│   │   │   └── news_analysis.py
│   │   ├── news_detail
│   │   │   ├── news_detail_page_resp.py
│   │   │   ├── news_detail_response_schema.py
│   │   │   └── news_detail_schema.py
│   │   ├── rss
│   │   │   └── rss_shema.py
│   │   ├── system_message
│   │   │   └── system_message.py
│   │   ├── user
│   │   │   ├── user_response_schema.py
│   │   │   └── user_schema.py
│   │   ├── user_push_category_wegiht
│   │   │   └── user_push_category_wegiht_schema.py
│   │   ├── user_push_config
│   │   │   └── user_push_config_schema.py
│   │   └── user_push_notify_channel
│   │       └── user_push_notify_channel_schema.py
│   ├── services                                # Service 业务服务
│   │   ├── ai_service.py
│   │   ├── article_storage_service.py
│   │   ├── baidu_rss_service.py
│   │   ├── category_service.py
│   │   ├── chat_message_service.py
│   │   ├── chat_session_service.py
│   │   ├── email_service.py
│   │   ├── file_service.py
│   │   ├── llm_api_log_service.py
│   │   ├── news_detail_service.py
│   │   ├── news_service.py
│   │   ├── policy_service.py
│   │   ├── rss_service.py
│   │   ├── user_push_config_service.py
│   │   └── user_service.py
│   ├── tasks                          # 任务
│   │   ├── ai_response.py                  # AI部分任务
│   │   ├── ai_task.py                      # celery 异步任务（绑定@celery_app.task(bind=True, name="ai.run_llm_task")）
│   │   ├── celery_app.py                   # celery 配置
│   │   ├── crwal_task.py                   # 爬虫任务
│   │   ├── email_sender.py                 # 邮件发送
│   │   └── scheduler.py                    # 定时任务（@scheduler_task.on_event("startup")）
│   └── utils                          # 工具类
│       ├── convert_json.py                 # json 转换
│       ├── fetch_full_text.py              # RSS 获取全文
│       ├── file_utils.py                   # 文件操作
│       ├── html_cleaner.py                 # html 清洗
│       ├── ip_util.py                      # ip
│       ├── jwt.py                          # jwt
│       ├── logger.py                       # 日志
│       ├── qrcode_utils.py                 # 二维码
│       ├── result_response.py              # API统一返回封装结果：{"code": 200, "message": "成功", "data": "数据"}
│       ├── time_convert.py                 # 时间转换
│       └── translator.py                   # 翻译
├── attach                             # 附件(作用于工具类中的文件操作 - 文件上传下载 - 个人demo直接放在项目中即可)
│   ├── audios
│   ├── docs
│   ├── images
│   ├── others
│   └── videos
├── docker                            # docker相关文件
│   └── Dockerfile
├── docker-compose.yml                  # docker-compose 生成环境使用
├── docker-dev-compose.yml              # docker-compose 开发环境使用
├── logs                              # 日志（个人demo直接放在项目中即可）
├── requirements.txt                  # 项目依赖包
├── sql                               # sql脚本，新环境下启动时，Docker会自动执行
│   ├── article_storage.sql
│   ├── baidu_rss_source.sql
│   ├── category.sql
│   ├── chat_message.sql
│   ├── chat_session.sql
│   ├── llm_api_log.sql
│   ├── news.sql
│   ├── news_detail.sql
│   ├── rss_source.sql
│   ├── script                          # 脚本(不参与项目，仅测试用)
│   │   ├── data
│   │   │   └── rss_list.xlsx
│   │   ├── full.py
│   │   └── rss.py
│   ├── system_message.sql
│   ├── user.sql
│   ├── user_push_category_weight.sql
│   ├── user_push_config.sql
│   ├── user_push_notify_channel.sql
│   └── users.sql
└── worker                            # 异步 RSS 网页爬取执行器
    └── rss_result_execute_worker.py
```

## 启动整个项目：
    项目目录执行： 
        docker compose up --build （生产环境）
        docker-compose -f docker-dev-compose.yml up --build （开发环境）

        启动流程：
            首次启动：
                docker compose build
            以后：
                docker compose up
            如果改动了代码：
                docker compose up --build api 或者 docker compose build api

