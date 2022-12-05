import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import requests
import yfinance as yf


from dao import YfinanceDao

from typing import List

def get_all_tickers() -> str:
    url = 'https://quality.data.gov.tw/dq_download_json.php'
    num_id = '11549'
    md5_check = 'bb878d47ffbe7b83bfc1b41d0b24946e'
    r = requests.get(f'{url}?nid={num_id}&md5_url={md5_check}')
    print(r.text, r.status_code)
    return [i["證券代號"] for i in r.json()]


def process_dataframe(stock, tickers=get_all_tickers()):
    columns = [ 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume' ]
    stocks = []
    for ticker in tickers:
        tmp_stock = stock[ [ (column, ticker) for column in columns] ].copy()
        tmp_stock.columns = columns
        tmp_stock['Ticker'] = ticker
        tmp_stock = tmp_stock[ ["Ticker"]+columns ]
        tmp_stock.reset_index(names='datetime', inplace=True)
        tmp_stock.dropna(subset=columns, how="all", axis=0, inplace=True)
        stocks += [ tmp_stock ]

    stock = pd.concat(stocks)
    stock.columns = [ ''.join(x.lower().split()) for x in stock.columns.tolist() ]
    return stock


def download_yesterday(db_initializer):
    print('download_yesterday')
    try:
        tickers = get_all_tickers()
    except:
        print('quality.data.gov.tw cannot get results')
        return
    tickers_TW = [ i+'.TW' for i in tickers ]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    stock = yf.download(
        tickers=tickers_TW,
        start=yesterday,
        end=yesterday,
        interval="1h", # minute
        ignore_tz=False
    )
    df_stocks = process_dataframe(stock, tickers)
    stocks_dicts: List[dict] = df_stocks.to_dict(orient='records')
    stocks_models: List[YfinanceDao] = [YfinanceDao(**d) for d in stocks_dicts]
    yfinanceDao: YfinanceDao = YfinanceDao()
    print(df_stocks)
    with db_initializer.db_session.begin() as sess:
        yfinanceDao.insert_bulk_do_nothing_on_conflict(sess, stocks_models)
    return
    