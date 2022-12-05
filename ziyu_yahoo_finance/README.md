
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
python3 -m unittest tests/config_test.py
python3 -m pip install sqlacodegen
sqlacodegen postgresql+psycopg2://admin:0000@db:5432/yahoo_stock  --outfile  dao/models/sqlacodegen_yfinance.py

```


12/01
we start from create firsts query by orm model
the first case is query a single time and ticket
and return a instance or none in database


then we unitest the results
we need to check i. the type call by dao_model
ii. the result is an instance of model

then the practice case is query the time interval results, and unitest by the map the results list

we now need to create an api
but note that  when we start an app of api

we need to load all the config and init module to start the app( in golang, the module may load before config if we not specified)

then we create the api folder in our project, and create the api which can show on swagger.


12/06
We design the router initialization step
in "init" and "init.api", also complete the startup, shutdown function
We add a new unitest for api which is reference in document in FastAPI.

Then 