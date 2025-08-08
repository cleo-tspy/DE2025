# Week 0 Starter — DE Projects

## Quick start
1) Install **uv** (optional but recommended): https://docs.astral.sh/uv/getting-started/  
   macOS/Linux:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2) Create venv & install:
   ```bash
   uv venv
   uv sync
   ```

   * Run

   ```
   source .venv/bin/activate
   ```

   * 2.1) 啟用 pre-commit（含祕密掃描與 ruff） // 把開發用工具裝進專案（並寫進 pyproject.toml / lock 檔）
   uv add --dev pre-commit detect-secrets ruff mypy pytest
   pre-commit install
   pre-commit run --all-files  # 先掃一次

   ```
   •	pre-commit：Git hooks 框架（幫你在 commit 前跑檢查）
	•	detect-secrets：掃出檔案裡的 API Key、密碼等
	•	ruff：Python 的 Lint/Format.「自動排版（ruff format）+ 靜態檢查（ruff check）」。等同 Black + flake8 + isort 合一；commit 前會自動跑，違規就擋下。
	•	mypy：型別檢查
	•	pytest：測試框架
   ```

3) Prepare env:
   ```bash
   cp .env.example .env  # edit values
   ```

4) Run demo:
   ```bash
   make demo
   ```

5) Run Bash mini exercises:
   ```bash
   bash scripts/w0_bash_exercises.sh
   ```

6) Lint / type / test:
   ```bash
   make lint
   make type
   make test
   ```

7) Enable pre-commit (secrets scan + ruff):
   ```bash
   uv add --dev pre-commit detect-secrets ruff mypy pytest
   pre-commit install
   pre-commit run --all-files
   ```

## Git flow (local → GitHub)
```bash
git init -b main
git add . && git commit -m "chore: init w0 starter"

# create feature branch, commit
git switch -c feat/w0-bash
# ...edit files...
git add . && git commit -m "feat(w0): bash exercises"
# push to your GitHub repo (replace URL)
git remote add origin https://github.com/<you>/de-projects.git
git push -u origin feat/w0-bash

# open PR (with GitHub CLI)
gh pr create --fill --base main --head feat/w0-bash

# simulate rebase workflow (after main moved ahead)
git switch feat/w0-bash
git fetch origin
git rebase origin/main
# resolve conflicts if any, then:
git push --force-with-lease
```
