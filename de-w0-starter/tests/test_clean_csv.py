from pathlib import Path
import pandas as pd
from etl.clean_csv import clean_with_dq


def test_bad_date_and_negative_amount(tmp_path: Path):
    src = tmp_path / "src.csv"
    src.write_text("date,amount\nBAD,50\n2025-08-02,-3\n")
    out_dir = tmp_path / "out"
    clean_with_dq(src, out_dir)
    dq = pd.read_csv(out_dir / "dq_report.csv")
    rules = set(dq["rule"].tolist())
    assert {"date_not_null", "amount_ge_0"} <= rules
