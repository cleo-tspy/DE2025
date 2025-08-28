from pathlib import Path
import pandas as pd
from etl.join import join_left


def test_left_join_missing_key(tmp_path: Path):
    orders = tmp_path / "orders.csv"
    customers = tmp_path / "customers.csv"
    orders.write_text("order_id,customer_id,amount\n1,10,100\n2,99,50\n")
    customers.write_text("customer_id,name\n10,Alice\n11,Bob\n")
    out = tmp_path / "joined.csv"

    join_left(orders, customers, out, on="customer_id")
    df = pd.read_csv(out)

    # customer_id=99 在右表缺失 → name 為 NaN
    row2 = df[df["order_id"] == 2].iloc[0]
    assert pd.isna(row2["name"])
