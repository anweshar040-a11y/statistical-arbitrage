import pandas as pd


def buy_and_hold_portfolio(prices):

    benchmark = prices.copy()

    benchmark["TCS Return"] = (
        benchmark["TCS"].pct_change().fillna(0)
    )

    benchmark["INFY Return"] = (
        benchmark["INFY"].pct_change().fillna(0)
    )

    benchmark["Benchmark Return"] = (
        benchmark["TCS Return"] * 0.5
        + benchmark["INFY Return"] * 0.5
    )

    initial_capital = 100000

    benchmark["Portfolio Value"] = (
        initial_capital
        * (1 + benchmark["Benchmark Return"]).cumprod()
    )

    benchmark["Running Peak"] = (
        benchmark["Portfolio Value"].cummax()
    )

    benchmark["Drawdown"] = (
        benchmark["Portfolio Value"]
        - benchmark["Running Peak"]
    ) / benchmark["Running Peak"]

    return benchmark