# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Numeric, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Yfinance(Base):
    __tablename__ = 'yfinance'

    datetime = Column(DateTime(True), primary_key=True, nullable=False)
    ticker = Column(String(10), primary_key=True, nullable=False)
    adjclose = Column(Numeric)
    close = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    open = Column(Numeric)
    volume = Column(BigInteger)
    createdat = Column(DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updatedat = Column(DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    deletedat = Column(DateTime(True))
