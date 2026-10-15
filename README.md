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

## 启动整个项目：
项目目录执行： 
    docker 一键启动会自动装配项目的基础设施：mysql, redis, rabbitMQ, Qdrant，以及创建mysql之后自动导入`/sql/*.sql`文件并运行，创建表结构
        `docker compose up --build` （prod 部署）
        `docker-compose -f docker-dev-compose.yml up --build` （dev 测试）

    启动流程：
        首次启动：
            `docker compose build`
        以后：
            `docker compose up`
        如果改动了代码：
            `docker compose up --build api` 或者 `docker compose build api`

    用户初始账号密码：
        admin/admin123
