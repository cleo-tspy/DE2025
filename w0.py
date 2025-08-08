# Create a starter bundle with Bash/Git/Python/Makefile/Secrets scaffolding
import os, textwrap, json, tarfile, io, pathlib, zipfile

root = "./data/de-w0-starter"
os.makedirs(root, exist_ok=True)

# Directory structure
dirs = [
    "src/app",
    "src/common",
    "tests",
    "data",
    "scripts",
]
for d in dirs:
    os.makedirs(os.path.join(root, d), exist_ok=True)

# Files content
pyproject = """\
[project]
name = "de-w0-starter"
version = "0.1.0"
description = "Week 0 starter for DE Projects"
requires-python = ">=3.10"
dependencies = [
  "pandas",
  "python-dotenv"
]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.mypy]
python_version = "3.10"
warn_unused_ignores = true
warn_redundant_casts = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
addopts = "-q"
pythonpath = ["src"]
"""

makefile = """\
.PHONY: install up test lint type demo precommit fmt

install:
\tuv sync

up:
\t@echo "No services yet; compose comes in Phase 1 Week 2"

test:
\tpytest

lint:
\truff check .

type:
\tmypy src

fmt:
\truff format .

demo:
\tpython -m app.demo

precommit:
\tpre-commit install
"""

gitignore = """\
# Python
__pycache__/
*.pyc
.venv/
.uv/
.mypy_cache/
.pytest_cache/
.dist-info/
.build/
/artifacts/

# Editors/OS
.DS_Store
.idea/
.vscode/

# Env & secrets
.env
*.pem
*.key
*.crt
secrets.*
"""

env_example = """\
# Copy this file to .env and fill values. Never commit .env
DB_URL=postgresql://user:pass@localhost:5432/app
API_KEY=changeme
"""

precommit = """\
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
"""

logging_setup = """\
from __future__ import annotations
import logging
import sys

def setup_logger(name: str = "app", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(module)s:%(lineno)d - %(message)s"
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(level)
        logger.propagate = False
    return logger
"""

demo_py = """\
from __future__ import annotations
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from common.logging_setup import setup_logger

logger = setup_logger("app.demo")

def main() -> None:
    load_dotenv()
    api_key = os.getenv("API_KEY", "<missing>")
    logger.info("Loaded API key length=%s", len(api_key))
    data_path = Path("data/sales.csv")
    if not data_path.exists():
        logger.warning("Sample data not found at %s", data_path)
        return
    df = pd.read_csv(data_path)
    logger.info("Rows=%d, TotalAmount=%.2f", len(df), df["amount"].sum())

if __name__ == "__main__":
    main()
"""

test_sanity = """\
def test_sanity():
    assert 1 + 1 == 2
"""

bash_exercises = """\
#!/usr/bin/env bash
# W0 Bash exercises — run: bash scripts/w0_bash_exercises.sh

set -euo pipefail

echo "[1/5] Generate sample files in ./data"
mkdir -p data
cat > data/access.log <<'LOG'
127.0.0.1 - - [08/Aug/2025:10:00:00 +0800] "GET / HTTP/1.1" 200 512
10.0.0.2 - - [08/Aug/2025:10:00:01 +0800] "GET /api HTTP/1.1" 500 128
127.0.0.1 - - [08/Aug/2025:10:00:02 +0800] "POST /login HTTP/1.1" 200 64
192.168.0.3 - - [08/Aug/2025:10:00:03 +0800] "GET /api HTTP/1.1" 502 64
10.0.0.2 - - [08/Aug/2025:10:00:04 +0800] "GET / HTTP/1.1" 404 32
LOG

cat > data/sales.csv <<'CSV'
date,city,amount
2025-08-01,Taipei,100.0
2025-08-01,Taichung,80.0
2025-08-02,Taipei,120.0
2025-08-02,Tainan,50.5
CSV

echo "[2/5] Pipeline: top status codes -> ./artifacts/status_top.txt"
mkdir -p artifacts
cut -d' ' -f9 data/access.log | sort | uniq -c | sort -nr > artifacts/status_top.txt
echo "Done. See artifacts/status_top.txt"

echo "[3/5] Redirection: extract errors -> ./artifacts/errors.log"
grep ' 5[0-9][0-9] ' data/access.log > artifacts/errors.log
echo "Done. See artifacts/errors.log"

echo "[4/5] grep/awk/sed mini tasks"
echo "- grep count 404 and 500-series"
grep -c ' 404 ' data/access.log | sed 's/^/404_count=/' > artifacts/grep_counts.txt
grep -c ' 5[0-9][0-9] ' data/access.log | sed 's/^/5xx_count=/' >> artifacts/grep_counts.txt

echo "- awk sum bytes column (field 10)"
awk '{sum+=$10} END{print sum}' data/access.log > artifacts/bytes_sum.txt

echo "- sed replace HTTP version with HTTP" 
sed -E 's#HTTP/[0-9.]+#HTTP#g' data/access.log > artifacts/access_clean.log

echo "[5/5] Show preview"
head -n 3 artifacts/status_top.txt || true
head -n 3 artifacts/errors.log || true

echo "All Bash tasks completed."
"""

readme = """\
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
"""

# Write files
files = {
    "pyproject.toml": pyproject,
    "Makefile": makefile,
    ".gitignore": gitignore,
    ".env.example": env_example,
    ".pre-commit-config.yaml": precommit,
    "src/common/logging_setup.py": logging_setup,
    "src/app/demo.py": demo_py,
    "tests/test_sanity.py": test_sanity,
    "scripts/w0_bash_exercises.sh": bash_exercises,
    "README.md": readme,
    "data/sales.csv": "date,city,amount\n2025-08-01,Taipei,100.0\n",
}
for rel, content in files.items():
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

# Make bash script executable
os.chmod(os.path.join(root, "scripts/w0_bash_exercises.sh"), 0o755)

# Create zip archive
zip_path = "./data/de-w0-starter.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            full = os.path.join(dirpath, name)
            arc = os.path.relpath(full, root)
            z.write(full, arc)

# zip_path