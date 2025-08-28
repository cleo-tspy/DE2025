.PHONY: install up test lint type demo precommit fmt

install:
	uv sync

up:
	@echo "No services yet; compose comes in Phase 1 Week 2"

.PHONY: test
test:
	PYTHONPATH=. uv run pytest -q

lint:
	ruff check .

type:
	mypy src

fmt:
	ruff format .

demo:
	PYTHONPATH=src python -m app.demo
	# 清理 + DQ 報告
	PYTHONPATH=. uv run python -c "from etl.clean_csv import clean_with_dq; clean_with_dq('data/sales.csv','artifacts/w1')"
	# 依日期聚合金額
	PYTHONPATH=. uv run python -c "from etl.aggregate import aggregate_daily_sales; aggregate_daily_sales('artifacts/w1/clean.csv','artifacts/w1/agg_daily.csv')"


precommit:
	pre-commit install
