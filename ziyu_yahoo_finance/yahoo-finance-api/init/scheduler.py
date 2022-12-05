import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from jobs import download_yesterday

def yfinance_crawler_scheduler(db_initializer) -> BackgroundScheduler:
    scheduler: BackgroundScheduler = BackgroundScheduler()
    scheduler.add_job(
        download_yesterday(db_initializer),
        trigger=CronTrigger.from_crontab('* * * * *')
    )
    return scheduler

# s = yfinance_crawler_scheduler()
# s.start()
# time.sleep(300)
# s.shutdown()
