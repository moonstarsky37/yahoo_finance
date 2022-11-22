from init.db import DbInitializer

db_initializer = DbInitializer()


def startup():
    db_initializer.migrate()


def shutdown():
    pass
