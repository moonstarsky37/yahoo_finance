
runDB:
	@docker compose up db -d

runApp:
	@cd app/ && uvicorn server:app --host 0.0.0.0 --port 8080

runTest:
	python3 -m unittest tests/test_yfinance_parser.py