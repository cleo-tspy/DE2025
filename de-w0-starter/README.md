# Week 1 — Reproduce（清理 → 聚合 → 產出）

**輸入**
- `data/sales.csv`（已提供示例）

**一鍵 Demo**
```bash
make demo
```

**手動指令（等同 demo）**
```bash
# 1) 清理 + DQ 報告（輸出到 artifacts/w1/）
PYTHONPATH=. uv run python -c "from etl.clean_csv import clean_with_dq; clean_with_dq('data/sales.csv','artifacts/w1')"

# 2) 依日期聚合金額（讀 clean.csv → 寫 agg_daily.csv）
PYTHONPATH=. uv run python -c "from etl.aggregate import aggregate_daily_sales; aggregate_daily_sales('artifacts/w1/clean.csv','artifacts/w1/agg_daily.csv')"
```

**輸出（artifacts/w1/）**
- `clean.csv`
- `dq_report.csv`
- `agg_daily.csv`

---

# Week 0 Starter — DE Projects

## Quick start
1) 安裝 **uv**（建議）：<https://docs.astral.sh/uv/getting-started/>
   - macOS/Linux
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```

2) 建立虛擬環境並安裝依賴
   ```bash
   uv venv
   uv sync
   ```

3) 準備環境變數
   ```bash
   cp .env.example .env  # 編輯對應值；請勿提交到 Git
   ```

4) 啟用 pre-commit（含祕密掃描與 ruff）
   ```bash
   uv add --dev pre-commit detect-secrets ruff mypy pytest
   pre-commit install
   pre-commit run --all-files  # 先掃一次
   ```
   - **pre-commit**：Git hooks 框架，commit 前自動檢查
   - **detect-secrets**：掃描 API key/密碼
   - **ruff**：格式化 + Lint（相當於 Black + flake8 + isort 合一）
   - **mypy**：型別檢查
   - **pytest**：測試框架

5) 常用指令
   ```bash
   make lint    # ruff check
   make type    # mypy
   make test    # PYTHONPATH=. uv run pytest -q
   make demo    # 產出 artifacts/w1/{clean.csv,dq_report.csv,agg_daily.csv}
   ```

6) Bash mini exercises（W0）
   ```bash
   bash scripts/w0_bash_exercises.sh
   ```

## Troubleshooting
- `ModuleNotFoundError: No module named 'etl'`：
  - 用 `make test` 或 `make demo`（已內建 `PYTHONPATH=.`），
  - 或手動在命令前加 `PYTHONPATH=.`。
- pandas 解析日期告警：若輸入格式固定為 `YYYY-MM-DD`，可在程式使用 `pd.to_datetime(..., format="%Y-%m-%d", errors="coerce", utc=True)` 消除警告。