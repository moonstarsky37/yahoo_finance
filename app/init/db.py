from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session

from configs import settings
from db.models.yfinance import YfinanceModel


class DbInitializer():
    def __init__(self) -> None:
        # do_echo: bool = True if settings().mode.upper(
        # ) in {'DEVELOPMENT', 'TEST', 'DEBUG'} else False
        self.db_engine: Engine = create_engine(
            settings().v0.db.dsn)
        self.db_session: Session = sessionmaker(
            bind=self.db_engine,
            expire_on_commit=False,
            class_=Session
        )

    def migrate(self):
        YfinanceModel.metadata.create_all(self.db_engine)
