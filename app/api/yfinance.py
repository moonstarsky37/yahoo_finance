import os
import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, status, Request

from api.schema.yfinance import YfinanceResponse, Yfinance

from init import db_initializer
from db.yfinance import YfinanceDao

logger: logging.Logger = logging.getLogger(__name__)

logger.info("Initialize yfinance_router_v0...")

yfinance_router_v0: APIRouter = APIRouter(
    prefix=os.path.join("/", "yfinance", "v0"),
    tags=["v0", "yfinance"]
)


@yfinance_router_v0.get("/", status_code=status.HTTP_200_OK, response_model=YfinanceResponse)
def get_last_by_ticker(ticker: str, request: Request):
    logger.info("Get request {}".format(request.base_url))
    yfinance = YfinanceDao()

    current: datetime = datetime.now()
    current_date_str: str = current.strftime("%Y-%m-%d")
    current_date: datetime = datetime.strptime(
        ' '.join([current_date_str, "00:00:00+08:00"]), "%Y-%m-%d %H:%M:%S%z")
    start, end = current_date, current_date+timedelta(days=1)

    res = []
    with db_initializer.db_session.begin() as sess:
        res = yfinance.get_yfinance_by_trange_and_ticker(
            session=sess,
            start=start,
            end=end,
            ticker=ticker
        )
        res = [
            Yfinance(**(m["YfinanceModel"].dict()))
            for m in res
        ]

    return YfinanceResponse(
        status_code=status.HTTP_200_OK,
        msg="Get {} success".format(ticker),
        data=res
    )
