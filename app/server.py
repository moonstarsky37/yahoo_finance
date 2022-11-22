from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

import init
from init.api import init_app
from jobs import init_scheduler

app: FastAPI = init_app()
scheduler: BackgroundScheduler = init_scheduler()


@app.on_event("startup")
def startup():
    init.startup()
    scheduler.start()


@app.on_event("shutdown")
def shutdown():
    init.shutdown()
    scheduler.shutdown()
