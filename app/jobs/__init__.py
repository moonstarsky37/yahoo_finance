from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from jobs.yfinance_parser import get_new_finance


def init_scheduler() -> BackgroundScheduler:
    scheduler: BackgroundScheduler = BackgroundScheduler()
    scheduler.add_job(
        get_new_finance,
        trigger=CronTrigger.from_crontab('0 0 * * *')
    )
    return scheduler
