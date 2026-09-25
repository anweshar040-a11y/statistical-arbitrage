import pandas as pd

from src.hedge_ratio import calculate_hedge_ratio
from src.statistics_utils import rolling_zscore
from src.strategy import generate_positions
from src.backtester import backtest_strategy
from src.performance_metrics import sharpe_ratio


def walk_forward_window(train_data, test_data):

    alpha, beta, model = calculate_hedge_ratio(
        train_data["TCS"],
        train_data["INFY"],
    )

    test = test_data.copy()

    test["Spread"] = (
        test["INFY"] - beta * test["TCS"]
    )

    test["Z-Score"] = rolling_zscore(
        test["Spread"]
    )

    signals = pd.DataFrame(index=test.index)

    signals["Signal"] = 0

    signals.loc[
        test["Z-Score"] > 2,
        "Signal",
    ] = -1

    signals.loc[
        test["Z-Score"] < -2,
        "Signal",
    ] = 1

    signals.loc[
        test["Z-Score"].abs() < 0.5,
        "Signal",
    ] = 0

    signals["Position"] = generate_positions(
        signals["Signal"]
    )

    results = backtest_strategy(
        test,
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
        "Train End": train_data.index[-1],
        "Test Start": test_data.index[0],
        "Test End": test_data.index[-1],
        "Sharpe": sharpe_ratio(results["Strategy Return"]),
        "Final Portfolio": results["Portfolio Value"].iloc[-1],
        "Drawdown": abs(results["Drawdown"].min()),
        "Trades": signals["Signal"].abs().sum(),
    }

    return metrics, results