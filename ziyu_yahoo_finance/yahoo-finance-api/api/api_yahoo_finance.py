from datetime import datetime

from fastapi import APIRouter, status, HTTPException, Query

import dao
from dao.models.postgresql_yfinance import YfinanceModel
from api.schema.yahoo_finance import GetYfinanceByTimeIntervalAndTickerResponse
from api.schema.yahoo_finance import YfinanceSchema
from init import db_initializer

from typing import List

yfinance_router: APIRouter = APIRouter(tags=['YFinance'])


@yfinance_router.get(
    '/',
    response_model=GetYfinanceByTimeIntervalAndTickerResponse, 
    status_code=status.HTTP_200_OK
)
def get_yfinance_by_time_interval_and_ticker(
    start_datetime_str:str, 
    end_datetime_str:str,
    ticker_code:str):
    print(start_datetime_str, end_datetime_str)
    t_format: str =  "%Y-%m-%d %H:%M:%S%z"
    # 2022-11-25 00:00:00+08:00
    try:
        start_datetime: datetime = datetime.strptime(start_datetime_str, t_format)
        print('start_datetime success')
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_datetime format not correct"
        )
        
    try:
        end_datetime: datetime = datetime.strptime(end_datetime_str, t_format)
        print('end_datetime success')
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_datetime format not correct"
        )
        
    res: List[YfinanceModel] = []
    with db_initializer.session.begin() as sess:
        try:
            res = dao.YfinanceDao.get_by_time_interval_and_ticker(
                sess, start_datetime, end_datetime,ticker_code)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='connection failed'
            )
    yfinance_schema: List[YfinanceSchema] = [
        YfinanceSchema(**r.as_dict()) for r in res
    ]
    # return GetYfinanceByTimeIntervalAndTickerResponse[status_code,msg,data]
    return GetYfinanceByTimeIntervalAndTickerResponse(
        status_code=status.HTTP_200_OK,
        msg='Query finished',
        data=yfinance_schema,
    )








@yfinance_router.get(
    '/tickers',
    response_model=GetYfinanceByTimeIntervalAndTickerResponse, 
    status_code=status.HTTP_200_OK
)
def get_yfinance_by_time_interval_and_tickers(
    start_datetime_str:str, 
    end_datetime_str:str,
    tickers_code:str):
    t_format: str =  "%Y-%m-%d %H:%M:%S%z"
    # 2022-11-25 00:00:00+08:00

    try:
        start_datetime: datetime = datetime.strptime(start_datetime_str, t_format)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_datetime format not correct"
        )
        
    try:
        end_datetime: datetime = datetime.strptime(end_datetime_str, t_format)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_datetime format not correct"
        )
    tickers_code = tickers_code.split(',')
        
    res: List[YfinanceModel] = []
    with db_initializer.session.begin() as sess:
        try:
            res = dao.YfinanceDao.get_by_time_interval_and_tickers(
                sess, start_datetime, end_datetime,tickers_code)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='connection failed'
            )
    yfinance_schema: List[YfinanceSchema] = [
        YfinanceSchema(**r.as_dict()) for r in res
    ]
    return GetYfinanceByTimeIntervalAndTickerResponse(
        status_code=status.HTTP_200_OK,
        msg='Query finished',
        data=yfinance_schema,
    )