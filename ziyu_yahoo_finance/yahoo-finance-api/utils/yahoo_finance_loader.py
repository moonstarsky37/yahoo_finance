import logging
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf


from typing import List, Union


logger: logging.Logger = logging.getLogger(__name__)


class FinanceLoader():

    def __init__(self) -> None:
        pass

    @staticmethod
    def split_ticker(tickers: str, tickers_spliter: str = ' ') -> List[str]:
        return tickers.split(tickers_spliter)

    @staticmethod
    def str_to_datetime(t: str) -> datetime:
        try:
            t: datetime = datetime.strptime(t, "%Y-%m-%d")
        except:
            logger.error(
                "time format error: \'{}\' not match in format \'%Y-%m-%d\'".format(t))
            return None
        return t

    @staticmethod
    def load_yfinance_by_tickers_an_time(
        tickers: Union[List[str], str],
        start: Union[datetime, str] = datetime.now(),
        end: Union[datetime, str] = datetime.now()+timedelta(days=1),
        interval: Union[str, None] = '1m',
        tickers_spliter: str = " "
    ) -> pd.DataFrame:

        tickers: List[str] = FinanceLoader.split_ticker(tickers, tickers_spliter) if isinstance(
            tickers, str) else tickers

        if isinstance(start, str):
            start = FinanceLoader.str_to_datetime(start)

        if isinstance(end, str):
            end = FinanceLoader.str_to_datetime(end)

        if (not start) or (not end):
            return None

        logger.info("Get stock, {}, from {} to {}".format(
            ' '.join(tickers), start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
        yf_res: pd.DataFrame = yf.download(
            tickers=tickers,
            start=start,
            end=end,
            interval=interval,
            ignore_tz=False
        )

        return None if yf_res.empty else yf_res

    @staticmethod
    def process_yf(
        res_yf: pd.DataFrame,
        tickers: Union[List[str], str],
        tickers_spliter: str = " ",
        columns: List[str] = ['Adj Close', 'Close',
                              'High', 'Low', 'Open', 'Volume']
    ) -> pd.DataFrame:
        logger.info("Process stocks...")

        tickers: List[str] = FinanceLoader.split_ticker(tickers, tickers_spliter) if isinstance(
            tickers, str) else tickers

        stocks = []
        for ticker in tickers:
            tmp_stock = res_yf[[(column, ticker) for column in columns]].copy() if len(
                tickers) > 1 else res_yf
            tmp_stock.columns = columns
            tmp_stock.dropna(subset=columns, how="all", axis=0, inplace=True)
            tmp_stock['Ticker'] = ticker
            tmp_stock = tmp_stock[["Ticker"]+columns]
            tmp_stock.reset_index(names='datetime', inplace=True)
            stocks += [tmp_stock]
        return pd.concat(stocks)

    def __call__(
        self,
        tickers: Union[List[str], str],
        start: Union[datetime, str] = datetime.now(),
        end: Union[datetime, str] = datetime.now()+timedelta(days=1),
        interval: Union[str, None] = '1m',
        tickers_spliter: str = " "
    ) -> pd.DataFrame:
        logger.info("FinanceLoader processing yfinance output...")

        tickers: List[str] = FinanceLoader.split_ticker(tickers, tickers_spliter) if isinstance(
            tickers, str) else tickers

        res_yf: pd.DataFrame = FinanceLoader.load_yfinance_by_tickers_an_time(
            tickers, start, end, interval)
        if res_yf.empty:
            logger.warn("The stock, {}, from {} to {} is empty".format(
                ' '.join(tickers), start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
            return None

        res_yf = FinanceLoader.process_yf(res_yf, tickers)
        logger.info("FinanceLoader processing yfinance output...finish")

        return res_yf


if __name__ == '__main__':
    loader = FinanceLoader()
    yf_res = loader(
        tickers="2330.TW 2451.TW",
        start=datetime.now()+timedelta(days=-5),
        end=datetime.now()
    )
    print(yf_res.head())
    print(yf_res.tail())
