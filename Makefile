install:
	poetry install

lint:
	poetry run flake8 brain_games

test:
	poetry run pytest

.PHONY: install lint test
