
## Create new project for practice
```bash=
touch Dockerfile docker-compose.yml Makefile .env
mkdir -p yahoo-finance-api/{init,configs,dao,utils,jobs,tests}
mkdir -p yahoo-finance-api/dao/models
```

* Inside container
```bash=
export APP_MODE=PROD
export APP_V0_DB_DSN='postgresql+psycopg2://admin:0000@db:5432/yahoo_stock'
sqlacodegen postgresql+psycopg2://admin:0000@db:5432/yahoo_stock  --outfile  dao/models/sqlacodegen_yfinance.py
```
