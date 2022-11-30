

runApp:
	@cd yahoo-finace-api/ && uvicorn server:app --host 0.0.0.0 --port 8080

cleanPyCache:
	python3 -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	python3 -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
