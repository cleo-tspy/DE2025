from __future__ import annotations
from pathlib import Path
import pandas as pd

"""
聚合 + Join 骨架與測試
"""


def aggregate_daily_sales(
    in_path: str | Path,
    out_path: str | Path,
    date_col: str = "date",
    value_col: str = "amount",
) -> None:
    df = pd.read_csv(in_path)

    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce", utc=True)
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")

    df = df.dropna(subset=[c for c in (date_col, value_col) if c in df.columns])

    # 以日期聚合（去除時間成分）
    if pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df["date_only"] = df[date_col].dt.date
    else:
        df["date_only"] = df[date_col]

    out_dir = Path(out_path).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    out = (
        df.groupby("date_only", as_index=False)[value_col]
        .sum()
        .rename(columns={"date_only": date_col})
    )
    out.to_csv(out_path, index=False)
