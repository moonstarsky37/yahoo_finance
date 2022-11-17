FROM ubuntu:20.04

ENV TZ=Asia/Taipei

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata && \
    apt-get install -y \
    git \
    curl \
    python3-pip \
    python3-dev  \
    && \
    apt-get clean && \
    python3 -m pip install requests numpy pandas psycopg2-binary sqlalchemy jupyter jupyterlab yfinance && \
    mkdir /app

WORKDIR /app

CMD jupyter-lab --config /app/jupyter_notebook_config.py