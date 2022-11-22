from fastapi import FastAPI

import init
from init.api import init_app

app: FastAPI = init_app()


@app.on_event("startup")
def startup():
    init.startup()
