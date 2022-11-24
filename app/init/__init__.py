from init.db import DbInitializer
from init.logger import LoggerInitializer

db_initializer = DbInitializer()

_ = LoggerInitializer('db', ['sqlalchemy'])
_ = LoggerInitializer('api', [])
_ = LoggerInitializer('utils', [])
_ = LoggerInitializer('jobs', [])


def startup():
    db_initializer.migrate()


def shutdown():
    pass
