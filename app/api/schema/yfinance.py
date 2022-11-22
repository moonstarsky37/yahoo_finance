from datetime import datetime

from pydantic import BaseModel


from typing import List


class Yfinance(BaseModel):
    datetime: datetime
    ticker: str
    adjclose: float
    close: float
    high: float
    low: float
    open: float
    volume: int
    updatedat: datetime


class YfinanceResponse(BaseModel):
    status_code: int
    msg: str
    data: List[Yfinance]
