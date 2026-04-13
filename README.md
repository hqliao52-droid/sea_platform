项目名称：内陆企业出海Mini APP设计
一、核心需求（Demend Analysis）：
利用 AI 帮助服务企业出海的机构降低公众号内容运营成本，并提升信息服务能力。
二、目标解决（Project）：
企业出海信息分散且获取效率低，同时公众号运营成本高，因此需要一个基于AI的信息处理平台，自动聚合、分析和生成出海相关内容，为企业提供高效的信息服务。
三、服务对象（Object）：
公众号运营团队、四川/内陆有出海需求的企业
四、核心模块（Model）:
1、信息采取
数据来源：行业公众号、政策网、出海资讯网站、各企业案例、新闻……
2、AI内容处理
利用AI 对信息自动完成：文章总结、topic聚类、keywords提炼、行业分类、政策识别……输出结构化的信息供以阅读/处理。
3、内容生成与运营
消息气泡：利用AI 对资讯自动生成类似《今日XXX企业出海咨询》----XXX代指服务端（一对一）
4、企业服务信息分发
企业登录账号后，可以使用今日出海资讯、AI问答、个性化内容推送……

目录架构：
sea_ai_platform
│
│  .env
│  docker-compose.yml
│  README.md
│  requirements.txt
│
├── app
│  ├── main.py                # FastAPI入口
│  ├─ai                     # AI处理
│  │      classifier.py
│  │      keyword_extract.py
│  │      summarizer.py
│  │
│  ├─api                    # API接口
│  │      ai_api.py
│  │      news_api.py
│  │      user_api.py
│  │
│  ├─config                # 配置
│  │      settings.py
│  │
│  ├─crawler                # 信息采集
│  │      news_spider.py
│  │      rss_spider.py
│  │
│  ├─database               # 数据库连接
│  │      mysql.py
│  │
│  ├─models                 # 数据库模型
│  │      news_model.py
│  │      policy_model.py
│  │      user_model.py
│  │
│  ├─schemas                # 数据结构
│  │      new_schema.py
│  │      user_schema.py
│  │
│  ├─services               # 业务逻辑
│  │      ai_service.py
│  │      news_service.py
│  │      policy_service.py
│  │
│  ├─tasks                  # Celery任务
│  │      ai_task.py           # AI处理任务
│  │      crwal_task.py        # 信息采集任务
│  │      celery_app.py        # Celery配置
│  │
│  └─utils                  # 工具
│          logger.py
│
├─docker                      # Docker镜像
│      Dockerfile
│
└─worker                     # Celery worker
        celery_worker.py

## 启动整个项目：
    项目目录执行： docker compose up --build
