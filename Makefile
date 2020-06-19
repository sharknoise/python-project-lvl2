install:
	poetry install

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest

test-coverage:
	poetry run pytest tests --cov=gendiff --cov-report xml

typecheck:
	poetry run mypy gendiff

.PHONY: install lint test test-coverage typecheck
