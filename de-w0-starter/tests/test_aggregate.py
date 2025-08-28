from pathlib import Path
import pandas as pd
from etl.aggregate import aggregate_daily_sales


def test_aggregate_sums_by_date(tmp_path: Path):
    src = tmp_path / "clean.csv"
    src.write_text("date,amount\n" "2025-08-01,100\n" "2025-08-01,50\n" "2025-08-02,10\n")
    out = tmp_path / "agg.csv"
    aggregate_daily_sales(src, out)

    df = pd.read_csv(out)
    # 總金額 160（100+50+10）
    assert df["amount"].sum() == 160
    # 兩天的彙總
    assert len(df) == 2
