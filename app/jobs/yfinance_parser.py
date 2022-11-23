from datetime import datetime, timedelta

import requests

from init import db_initializer
from utils import FinanceLoader
from db.yfinance import YfinanceDao
from db.models.yfinance import YfinanceModel

from typing import List


def get_all_tickers() -> List[str]:
    r = requests.get(
        'https://quality.data.gov.tw/dq_download_json.php?nid=11549&md5_url=bb878d47ffbe7b83bfc1b41d0b24946e')
    return [i["證券代號"] for i in r.json()]


def get_new_finance():
    loader = FinanceLoader()
    tickers = [i+'.TW' for i in get_all_tickers()]
    yf_res = loader(
        tickers=tickers,
        start=datetime.now()+timedelta(days=-1),
        end=datetime.now()
    )
    if yf_res.empty:
        return

    yf_res_dicts: List[dict] = yf_res.to_dict(orient='record')
    yf_res_models: List[YfinanceModel] = [
        YfinanceModel(**d) for d in yf_res_dicts]
    yfinanceDao: YfinanceDao = YfinanceDao()
    with db_initializer.db_session.begin() as sess:
        yfinanceDao.insert_bulk(sess, yf_res_models)
    return
