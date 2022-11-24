# coding: utf-8
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP, NUMERIC, VARCHAR

from db.models import BaseModel


class YfinanceModel(BaseModel):
    __tablename__ = 'yfinance'

    datetime = Column(TIMESTAMP, primary_key=True)
    ticker = Column(VARCHAR(10), primary_key=True)
    adjclose = Column(NUMERIC)
    close = Column(NUMERIC)
    high = Column(NUMERIC)
    low = Column(NUMERIC)
    open = Column(NUMERIC)
    volume = Column(BIGINT)
    createdat = Column(TIMESTAMP)
    updatedat = Column(TIMESTAMP)
    deletedat = Column(TIMESTAMP)
