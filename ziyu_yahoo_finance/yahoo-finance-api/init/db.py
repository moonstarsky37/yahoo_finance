
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dao.models.postgresql_yfinance import YfinanceModel
from configs import settings


class DbInitializer():
    def __init__(self) -> None:

        do_echo: bool = settings().mode.upper() in ['DEV', 'DEVELOPMENT', 'DEBUG']
        self.engine: Engine = create_engine(
            settings().v0.db.dsn, 
            echo=do_echo)
        self.session: Session = sessionmaker(
            bind=self.engine, 
            expire_on_commit=False,
            class_=Session
        )
    
    def migrate(self):
        YfinanceModel.metadata.create_all(self.engine)
