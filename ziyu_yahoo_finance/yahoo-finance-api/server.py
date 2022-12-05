import configs as _

# from apscheduler.schedulers.background import BackgroundScheduler


import init
from init.api import app
from init import yf_crawler_scheduler

@app.on_event('startup')
def startup():
    init.startup()
    yf_crawler_scheduler.start()


@app.on_event('shutdown')
def shutdown():
    init.shutdown()
    yf_crawler_scheduler.shutdown()
