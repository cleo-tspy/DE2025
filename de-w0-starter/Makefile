.PHONY: install up test lint type demo precommit fmt

install:
	uv sync

up:
	@echo "No services yet; compose comes in Phase 1 Week 2"

test:
	pytest

lint:
	ruff check .

type:
	mypy src

fmt:
	ruff format .

demo:
	PYTHONPATH=src python -m app.demo

precommit:
	pre-commit install
