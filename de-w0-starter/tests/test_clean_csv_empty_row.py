from pathlib import Path
import pandas as pd
from etl.clean_csv import clean_with_dq


def test_empty_row_dropped_and_dq_written(tmp_path: Path):
    src = tmp_path / "src.csv"
    # 一筆空列（逗點後留空），另外兩筆有效資料
    src.write_text("date,amount\n2025-08-01,100\n,\n2025-08-02,50\n")
    out_dir = tmp_path / "out"

    clean_with_dq(src, out_dir)

    # 清理後應只剩有效兩筆
    cleaned = pd.read_csv(out_dir / "clean.csv")
    assert len(cleaned) == 2

    # DQ 報告存在（空列會導致 date_not_null 規則觸發）
    dq = pd.read_csv(out_dir / "dq_report.csv")
    assert not dq.empty
    assert (dq["rule"] == "date_not_null").any()
