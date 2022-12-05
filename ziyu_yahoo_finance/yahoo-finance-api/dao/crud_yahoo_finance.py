from dao.models.postgresql_yfinance import YfinanceModel
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import and_, or_
from typing import List

class YfinanceDao():
    def __init__(self) -> None:
        pass
    

    @staticmethod
    def get_by_time_and_ticker(session: Session, t: datetime, ticker:str) -> YfinanceModel:
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