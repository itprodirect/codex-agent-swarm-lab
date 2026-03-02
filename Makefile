.PHONY: install test lint fmt run

install:
	python -m pip install -U pip
	python -m pip install -e ".[dev]"

test:
	python -m pytest -q

lint:
	python -m ruff check .
	python -m ruff format --check .

fmt:
	python -m ruff check . --fix
	python -m ruff format .

run:
	python -m agent_lab --help
