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
