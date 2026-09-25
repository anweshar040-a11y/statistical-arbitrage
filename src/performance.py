import pandas as pd


def performance_summary(results, trade_log):
    summary = {}

    summary["Initial Capital"] = results["Portfolio Value"].iloc[0]
    summary["Final Portfolio Value"] = results["Portfolio Value"].iloc[-1]

    summary["Total Return (%)"] = (
        (results["Portfolio Value"].iloc[-1]
         / results["Portfolio Value"].iloc[0] - 1)
        * 100
    )

    summary["Total Trades"] = len(trade_log)

    wins = trade_log["Return"] > 0
    losses = trade_log["Return"] <= 0

    summary["Winning Trades"] = wins.sum()
    summary["Losing Trades"] = losses.sum()

    if len(trade_log) > 0:
        summary["Win Rate (%)"] = wins.mean() * 100
        summary["Average Trade Return (%)"] = (
            trade_log["Return"].mean() * 100
        )
    else:
        summary["Win Rate (%)"] = 0
        summary["Average Trade Return (%)"] = 0

    summary["Maximum Drawdown (%)"] = (
        results["Drawdown"].min() * 100
    )

    return pd.DataFrame([summary])