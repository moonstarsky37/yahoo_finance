from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from sqlalchemy.dialects.postgresql import insert

from dao.models.postgresql_yfinance import YfinanceModel

from typing import List

class YfinanceDao():
    def __init__(self) -> None:
        pass
    

    @staticmethod
    def get_by_time_and_ticker(
        session: Session, 
        t: datetime, 
        ticker:str) -> YfinanceModel:
        return session.query(YfinanceModel).filter(
            and_(
                YfinanceModel.datetime==t,
                YfinanceModel.ticker==ticker
            )
        ).one_or_none()


    @staticmethod
    def get_by_time_interval_and_ticker(
        session: Session, 
        start_t: datetime,
        end_t: datetime,
        ticker:str) -> YfinanceModel:
        return session.query(YfinanceModel).filter(
            and_(
                YfinanceModel.ticker==ticker,
                YfinanceModel.datetime.between(start_t, end_t)
            )
        ).all()

    @staticmethod
    def get_by_time_interval_and_tickers(
        session: Session, 
        start_t: datetime,
        end_t: datetime,
        tickers:List[str]) -> YfinanceModel:
        return  session.query(YfinanceModel).filter(
            and_(
                YfinanceModel.datetime.between(start_t, end_t),
                YfinanceModel.ticker.in_(tickers)
            )
            
        ).all()


    @staticmethod
    def insert_bulk_do_nothing_on_conflict(
        session: Session, 
        models: List[YfinanceModel]) -> None:
        datas = [i.as_dict() for i in models]
        insert_statement = insert(YfinanceModel).values(datas)
        upsert_statement = insert_statement.on_conflict_do_nothing(
            constraint=f"{YfinanceModel.__tablename__}_pkey"
        )
        session.execute(upsert_statement)
        session.commit()

    