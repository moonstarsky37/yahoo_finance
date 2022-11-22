import time
from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware

from configs import settings


def create_base_app():
    if settings().mode.upper() in {'DEV', 'TEST', 'DEBUG', 'DEVELOPMENT'}:
        return FastAPI(docs_url='/docs', redoc_url='/redoc', openapi_url='/openapi.json')
    else:
        return FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


def create_app() -> FastAPI:
    app: FastAPI = create_base_app()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    return app
