#!/usr/bin/python3
from init.db import DbInitializer
from init.logger import LoggerInitializer
# from init.api import app
db_initializer = DbInitializer()

_ = LoggerInitializer('db', ['sqlalchemy'])
_ = LoggerInitializer('api', [])
_ = LoggerInitializer('jobs', [])


def startup():
    db_initializer.migrate()


def shutdown():
    db_initializer.session.close_all()
    db_initializer.engine.dispose()
    
