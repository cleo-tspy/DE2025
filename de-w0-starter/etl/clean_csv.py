from __future__ import annotations
from pathlib import Path
import pandas as pd


def clean_with_dq(in_path: str | Path, out_dir: str | Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(in_path)

    # 型別標準化
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)
    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # DQ 最小集
    issues = []
    if "date" in df and df["date"].isna().any():
        issues.append({"rule": "date_not_null", "failed": int(df["date"].isna().sum())})
    if "amount" in df and (df["amount"] < 0).any():
        issues.append({"rule": "amount_ge_0", "failed": int((df["amount"] < 0).sum())})
    pd.DataFrame(issues).to_csv(out_dir / "dq_report.csv", index=False)

    # 清理輸出
    df.dropna(subset=[c for c in ("date", "amount") if c in df.columns]).to_csv(
        out_dir / "clean.csv", index=False
    )
