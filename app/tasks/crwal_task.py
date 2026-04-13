from app.services.rss_service import RssSourceOperator
from app.utils.logger import Logger
from app.core.scheduler import scheduler
from app.crawler.news_spider import run_single_rss_task

rss_sources = RssSourceOperator()
logger = Logger.setup_logger(Logger.set_file_date())
async def spider_rss():
    ## rss源列表
    rss_list = rss_sources.get_active_rss_sources()

    ## 清空旧任务
    scheduler.remove_all_jobs()

    for rss in rss_list:
        rss_id = rss.id
        rss_name = rss.name
        url = rss.url
        minutes = rss.update_rate

        scheduler.add_job(
            run_single_rss_task,
            args=[rss_name, url],
            trigger="interval",
            minutes=minutes,
            id=f"rss_task_{rss_id}",
            replace_existing=True
        )
        logger.info(f"已调度：{rss_name} 每 {minutes} 分钟爬取一次！")
    
    for rss in rss_list:
        await run_single_rss_task(rss.name, rss.url)

