import pandas as pd


def rolling_zscore(series, window=30):
    """
    Calculate rolling Z-score.
    """

    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()

    zscore = (series - rolling_mean) / rolling_std

    return zscore