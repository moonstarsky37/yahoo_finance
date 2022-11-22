from fastapi import FastAPI, APIRouter

from api import create_app
from api.yfinance import yfinance_router_v0


def init_app() -> FastAPI:
    app: FastAPI = create_app()
    app.include_router(yfinance_router_v0)
    return app
