import logging
import pandas as pd
from datetime import timedelta, date, datetime
import yfinance as yf

from dao import YfinanceDao
from dao.models.postgresql_yfinance import YfinanceModel
from utils import FinanceLoader
from configs import settings

from typing import List


logger: logging.Logger = logging.getLogger(__name__)


def get_all_tickers() -> str:
    url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_data'
    df_tickers_data = pd.read_csv(f'{url}')
    return list(df_tickers_data["證券代號"].values)


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


def insert_stocks_models(db_session) -> List[YfinanceModel]:
    logger.info("Getting yfinance stock...")
    loader = FinanceLoader()
    is_settings_dev_mode = settings().mode.upper() in [
        'DEV', 'DEVELOPMENT', 'DEBUG']
    if is_settings_dev_mode:
        tickers = ['0050.TW', '2330.TW']
        yf_res = loader(
            tickers=tickers,
            start='2022-12-01',
            end='2022-12-03',
            interval='1d'
        )
    else:
        tickers = [i+'.TW' for i in get_all_tickers()]
        yf_res = loader(
            tickers=tickers,
            start=datetime.now()+timedelta(days=-1),
            end=datetime.now()
        )
    if yf_res.empty:
        return

    yf_res.columns = [''.join(x.lower().split())
                      for x in yf_res.columns.tolist()]

    yf_res_dicts: List[dict] = yf_res.to_dict(orient='records')

    yfinanceDao: YfinanceDao = YfinanceDao()

    stocks_models: List[YfinanceModel] = [
        YfinanceModel(**d) for d in yf_res_dicts]
    with db_session.begin() as sess:
        fetch_results: List[YfinanceModel] = yfinanceDao. \
            insert_bulk_do_nothing_on_conflict(
                sess, stocks_models)
        if is_settings_dev_mode:
            sess.rollback()
        else:
            sess.commit()
    return fetch_results
