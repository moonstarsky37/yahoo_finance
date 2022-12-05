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
    python3 -m pip install \
        requests==2.28.1 \
        numpy==1.23.4 \
        pandas==1.5.1 \
        psycopg2-binary==2.9.5 \
        sqlalchemy==1.4.44 \
        yfinance==0.1.87 \
        uvicorn==0.20.0 \
        fastapi==0.88.0 \
        Pillow \
        imgur-python\
        jupyter \
        jupyterlab \
    && \
    mkdir /app

WORKDIR /app

CMD jupyter-lab --config /app/jupyter_notebook_config.py