import pandas as pd

from datetime import timedelta, date
import yfinance as yf


from dao import YfinanceDao
from dao.models.postgresql_yfinance import YfinanceModel

from typing import List


def get_all_tickers() -> str:
    url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_data'
    df_tickers_data = pd.read_csv(f'{url}')
    return list(df_tickers_data["證券代號"].values)


def process_dataframe(
        stock: pd.DataFrame,
        tickers: List[str] = get_all_tickers()) -> pd.DataFrame:
    columns = ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
    stocks = []
    for ticker in tickers:
        tmp_stock = stock[[(column, ticker) for column in columns]].copy()
        tmp_stock.columns = columns
        tmp_stock['Ticker'] = ticker
        tmp_stock = tmp_stock[["Ticker"]+columns]
        tmp_stock.reset_index(names='datetime', inplace=True)
        tmp_stock.dropna(subset=columns, how="all", axis=0, inplace=True)
        stocks += [tmp_stock]

    stock = pd.concat(stocks)
    stock.columns = [''.join(x.lower().split())
                     for x in stock.columns.tolist()]
    return stock


def download_yesterday() -> List[YfinanceModel]:
    try:
        tickers = ['2330', '0050']  # get_all_tickers()
    except:
        print('get_all_tickers() cannot get results')
        return
    tickers_TW = [i+'.TW' for i in tickers]
    yesterday = date.today() - timedelta(days=1)
    stock = yf.download(
        tickers=tickers_TW,
        start=yesterday.strftime("%Y-%m-%d"),
        end=date.today().strftime("%Y-%m-%d"),
        interval="1h",  # minute
        ignore_tz=False
    )
    df_stocks = process_dataframe(stock, tickers_TW)
    stocks_dicts: List[dict] = df_stocks.to_dict(orient='records')
    stocks_models: List[YfinanceModel] = [
        YfinanceModel(**d) for d in stocks_dicts]
    return stocks_models


def insert_stocks_models(db_session, commit: bool = True) -> list:
    yfinanceDao: YfinanceDao = YfinanceDao()
    stocks_models: List[YfinanceModel] = download_yesterday()
    with db_session.begin() as sess:
        fetch_results = yfinanceDao.insert_bulk_do_nothing_on_conflict(
            sess, stocks_models, commit=commit)
    return fetch_results
