import pandas as pd
import yfinance as yf

from src.config import RAW_DATA


def download_stock(symbol, start, end):
    df = yf.download(
        symbol,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
    )

    # Fix yfinance's multi-level columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.index.name = "Date"

    df.to_csv(RAW_DATA / f"{symbol}.csv")

    return df


def load_stock(symbol):
    return pd.read_csv(
        RAW_DATA / f"{symbol}.csv",
        index_col="Date",
        parse_dates=True,
    )