from datetime import datetime
from app.services.rss_service import RssSourceOperator
from app.utils.log import logger
from app.core.scheduler import scheduler
from app.crawler.news_spider import crawl_all_rss_sources

rss_sources = RssSourceOperator()

async def spider_rss():
    """这个函数的唯一职责：同步数据库中的 RSS 源到调度器中"""
    rss_list = await rss_sources.get_active_rss_sources()

    # 警告：remove_all_jobs 会清空所有任务。如果你有非 RSS 的任务，建议加前缀并过滤
    # 为了安全，建议只移除 rss_task 开头的任务
    for job in scheduler.get_jobs():
        if job.id.startswith("rss_task_"):
            scheduler.remove_job(job.id)

    for rss in rss_list:
        rss_id = rss.id
        rss_name = rss.name
        url = rss.url
        minutes = rss.update_rate

        scheduler.add_job(
            crawl_all_rss_sources,
            args=[url],
            trigger="interval",
            minutes=minutes,
            id=f"rss_task_{rss_id}",
            replace_existing=True,
            # 让调度器在注册后立刻在后台跑一次，不用 await 死等
            next_run_time=datetime.now() 
        )
        logger.info(f"已调度：{rss_name} 每 {minutes} 分钟爬取一次！")
