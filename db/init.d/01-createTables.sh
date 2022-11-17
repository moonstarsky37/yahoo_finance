#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE TABLE IF NOT EXISTS yfinance (
        Datetime TIMESTAMPTZ,
        Ticker VARCHAR(10),
        AdjClose DECIMAL,
        Close DECIMAL,
        High DECIMAL,
        Low DECIMAL,
        Open DECIMAL,
        Volume BIGINT,

        PRIMARY KEY (Datetime, Ticker)
    );
EOSQL