#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE FUNCTION update_modified_column()   
    RETURNS TRIGGER AS \$\$
    BEGIN
        NEW.UpdatedAt = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    \$\$ language 'plpgsql';

	CREATE TABLE IF NOT EXISTS yfinance (
        Datetime TIMESTAMPTZ,
        Ticker VARCHAR(10),
        AdjClose DECIMAL,
        Close DECIMAL,
        High DECIMAL,
        Low DECIMAL,
        Open DECIMAL,
        Volume BIGINT,
        CreatedAt TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
        DeletedAt TIMESTAMPTZ,

        PRIMARY KEY (Datetime, Ticker)
    );

    CREATE TRIGGER update_ncdr_updatedat
    BEFORE UPDATE
    ON yfinance
    FOR EACH ROW
    EXECUTE PROCEDURE update_modified_column()
    ;

EOSQL