from fastapi import FastAPI
from api import create_app
from api.api_yahoo_finance import yfinance_router

def include_router(app: FastAPI):
    app.include_router(yfinance_router, prefix='/yfinance', tags=['YFinance'])

#!TODO Add version control

app: FastAPI = create_app()


include_router(app)