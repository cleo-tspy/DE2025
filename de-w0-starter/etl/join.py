from __future__ import annotations
from pathlib import Path
from typing import Sequence
import pandas as pd


def join_left(
    left_path: str | Path,
    right_path: str | Path,
    out_path: str | Path,
    on: str | Sequence[str],
) -> None:
    left = pd.read_csv(left_path)
    right = pd.read_csv(right_path)
    out_dir = Path(out_path).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    merged = left.merge(right, how="left", on=on)
    merged.to_csv(out_path, index=False)
