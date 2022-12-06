from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from jobs import insert_stocks_models


def yfinance_crawler_scheduler(db_session) -> BackgroundScheduler:

    scheduler: BackgroundScheduler = BackgroundScheduler()
    scheduler.add_job(
        insert_stocks_models,
        args=[db_session],
        trigger=CronTrigger.from_crontab('* * * * *')
    )
    return scheduler

# s = yfinance_crawler_scheduler()
# s.start()
# time.sleep(300)
# s.shutdown()
