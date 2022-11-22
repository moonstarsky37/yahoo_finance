import logging
from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.sql.expression import select
from sqlalchemy.orm import Session

from db.models.yfinance import YfinanceModel

from typing import List


class YfinanceDao():
    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(__name__)

    @staticmethod
    def get_yfinance_by_t_and_ticker(session: Session, t: datetime, ticker: str) -> YfinanceModel:
        return session.query(YfinanceModel).filter(
            and_(
                YfinanceModel.datetime == t,
                YfinanceModel.ticker == ticker
            )
        ).one_or_none()

    @staticmethod
    def get_yfinance_by_trange_and_ticker(session: Session, start: datetime, end: datetime, ticker: str) -> List[YfinanceModel]:
        stamt = select(
            YfinanceModel
        ).select_from(
            YfinanceModel
        ).where(
            and_(
                YfinanceModel.datetime >= start,
                YfinanceModel.datetime <= end,
                YfinanceModel.ticker == ticker
            )
        )
        res = session.execute(stamt)
        return res.fetchall()

    @staticmethod
    def get_yfinance_by_trange_and_tickers(session: Session, start: datetime, end: datetime, tickers: List[str]) -> List[YfinanceModel]:
        return session.query(YfinanceModel).filter(
            and_(
                YfinanceModel.datetime >= start,
                YfinanceModel.datetime <= end,
                YfinanceModel.ticker.in_(tickers)
            )
        ).all()

    @staticmethod
    def insert(session: Session, model: YfinanceModel) -> None:
        session.add(model)
        session.commit()

    @staticmethod
    def insert_bulk(session: Session, models: List[YfinanceModel]) -> None:
        session.bulk_save_objects(models)
        session.commit()


if __name__ == "__main__":
    import os
    import pandas as pd
    from datetime import timedelta
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    dsn = os.getenv('APP_V0__DB__DSN')
    engine = create_engine(dsn, echo=True)
    session = sessionmaker(bind=engine)

    current_date = datetime.strptime(
        '2022-11-21 00:00:00+08:00', "%Y-%m-%d %H:%M:%S%z")

    res = []
    with session.begin() as sess:
        yfinance = YfinanceDao()
        start, end = current_date, current_date+timedelta(days=1)
        print(start)
        print(end)
        res = yfinance.get_yfinance_by_trange_and_ticker(
            session=sess, start=start, end=end, ticker="2330.TW")
        res = map(lambda m: m["YfinanceModel"].dict(), res)
        res = pd.DataFrame(list(res))
    print(res.head())
