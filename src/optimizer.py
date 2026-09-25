import pandas as pd

from src.statistics_utils import rolling_zscore
from src.strategy import generate_positions
from src.backtester import backtest_strategy
from src.performance_metrics import (
    sharpe_ratio,
    annualized_return,
    annualized_volatility,
)


def run_strategy(prices, beta, entry_z, exit_z):

    data = prices.copy()

    data["Z-Score"] = rolling_zscore(
        data["Spread"]
    )

    signals = pd.DataFrame(index=data.index)

    signals["Signal"] = 0

    signals.loc[
        data["Z-Score"] > entry_z,
        "Signal",
    ] = -1

    signals.loc[
        data["Z-Score"] < -entry_z,
        "Signal",
    ] = 1

    signals.loc[
        data["Z-Score"].abs() < exit_z,
        "Signal",
    ] = 0

    signals["Position"] = generate_positions(
        signals["Signal"]
    )

    results = backtest_strategy(
        data,
        signals,
        beta,
    )

    initial_capital = 100000

    results["Portfolio Value"] = (
        initial_capital
        * (1 + results["Strategy Return"]).cumprod()
    )

    results["Running Peak"] = (
        results["Portfolio Value"].cummax()
    )

    results["Drawdown"] = (
        results["Portfolio Value"]
        - results["Running Peak"]
    ) / results["Running Peak"]

    metrics = {
        "Entry Z": entry_z,
        "Exit Z": exit_z,
        "Final Portfolio": results["Portfolio Value"].iloc[-1],
        "Sharpe": sharpe_ratio(results["Strategy Return"]),
        "Annual Return": annualized_return(results["Strategy Return"]),
        "Annual Volatility": annualized_volatility(results["Strategy Return"]),
        "Max Drawdown": abs(results["Drawdown"].min()),
        "Trades": signals["Signal"].abs().sum(),
    }

    return metrics, results