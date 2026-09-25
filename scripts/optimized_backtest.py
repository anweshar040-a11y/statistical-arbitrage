import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import pandas as pd

from src.data_loader import load_stock
from src.hedge_ratio import calculate_hedge_ratio
from src.statistics_utils import rolling_zscore
from src.strategy import generate_positions
from src.backtester import (
    backtest_strategy,
    create_trade_log,
)

tcs = load_stock("TCS.NS")
infy = load_stock("INFY.NS")

prices = pd.concat(
    [tcs["Close"], infy["Close"]],
    axis=1
).dropna()

prices.columns = ["TCS", "INFY"]

alpha, beta, model = calculate_hedge_ratio(
    prices["TCS"],
    prices["INFY"]
)

prices["Spread"] = (
    prices["INFY"]
    - beta * prices["TCS"]
)

prices["Z-Score"] = rolling_zscore(
    prices["Spread"]
)

signals = pd.DataFrame(index=prices.index)

signals["Signal"] = 0

signals.loc[
    prices["Z-Score"] > 2,
    "Signal"
] = -1

signals.loc[
    prices["Z-Score"] < -2,
    "Signal"
] = 1

signals.loc[
    prices["Z-Score"].abs() < 0.5,
    "Signal"
] = 0

signals["Position"] = generate_positions(
    signals["Signal"]
)


results = backtest_strategy(prices, signals,beta)

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

trade_log = create_trade_log(results)

results.to_csv(
    "results/tables/optimized_equity_curve.csv"
)

trade_log.to_csv(
    "results/tables/optimized_trade_log.csv",
    index=False
)

plt.figure(figsize=(12, 5))

plt.plot(
    results.index,
    results["Portfolio Value"],
    label="Optimized Strategy"
)

plt.title("Optimized Equity Curve")
plt.xlabel("Date")
plt.ylabel("Portfolio Value (₹)")
plt.legend()

plt.tight_layout()

plt.savefig(
    "results/figures/optimized_equity_curve.png"
)

plt.close()

plt.figure(figsize=(12, 5))

plt.fill_between(
    results.index,
    results["Drawdown"] * 100,
    0
)

plt.title("Drawdown Curve")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")

plt.tight_layout()

plt.savefig(
    "results/figures/drawdown_curve.png"
)

plt.close()
print("\nLowest Portfolio Value:")
print(results["Portfolio Value"].min())

print("\nHighest Portfolio Value:")
print(results["Portfolio Value"].max())

print("\nMaximum Drawdown (%):")
print(results["Drawdown"].min() * 100)

print("OLS Hedge Ratio:", round(beta, 4))
print("Final Portfolio Value:", round(results["Portfolio Value"].iloc[-1], 2))
print("Maximum Drawdown:", round(results["Drawdown"].min(), 4))
print("Total Trades:", len(trade_log))