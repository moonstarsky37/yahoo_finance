#!/usr/bin/python3
from init.db import DbInitializer
from init.logger import LoggerInitializer
from init.scheduler import yfinance_crawler_scheduler

db_initializer = DbInitializer()
yf_crawler_scheduler = yfinance_crawler_scheduler(db_initializer)

_ = LoggerInitializer('db', ['sqlalchemy'])
_ = LoggerInitializer('api', [])
_ = LoggerInitializer('jobs', [])


def startup():
    db_initializer.migrate()


def shutdown():
    db_initializer.session.close_all()
    db_initializer.engine.dispose()
    
