from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = ROOT / "data" / "raw"
PROCESSED_DATA = ROOT / "data" / "processed"

START_DATE = "2021-01-01"
END_DATE = "2026-08-01"

NIFTY_STOCKS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "LT.NS",
    "ITC.NS",
    "BHARTIARTL.NS",
    "KOTAKBANK.NS"
]