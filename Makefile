.PHONY: run test

run:
	poetry run flask --app user_monitoring.main:app run --debug

stop:
	lsof -t -i :5000 | xargs kill -9

test:
	poetry run python -m pytest -vvv
