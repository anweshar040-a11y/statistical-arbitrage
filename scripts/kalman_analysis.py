import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import load_stock
from src.kalman_filter import kalman_hedge_ratio
from src.dynamic_spread import create_dynamic_spread
from src.statistics_utils import rolling_zscore
from src.strategy import generate_positions
from src.backtester import (
    backtest_strategy,
    create_trade_log,
)

# Load stock prices
tcs = load_stock("TCS.NS")
infy = load_stock("INFY.NS")

prices = pd.concat(
    [tcs["Close"], infy["Close"]],
    axis=1,
).dropna()

prices.columns = ["TCS", "INFY"]

# Kalman hedge ratio
prices["Kalman Beta"] = kalman_hedge_ratio(
    prices["TCS"],
    prices["INFY"],
)

# Dynamic spread
prices["Dynamic Spread"] = create_dynamic_spread(
    prices,
    prices["Kalman Beta"],
)

# Rolling Z-score
prices["Z-Score"] = rolling_zscore(
    prices["Dynamic Spread"],
)

# Save beta table
prices.to_csv(
    "results/tables/kalman_beta.csv"
)

# Plot dynamic hedge ratio
plt.figure(figsize=(12, 5))

plt.plot(
    prices.index,
    prices["Kalman Beta"],
)

plt.title("Dynamic Hedge Ratio (Kalman Filter)")
plt.xlabel("Date")
plt.ylabel("Beta")

plt.tight_layout()

plt.savefig(
    "results/figures/kalman_beta.png"
)

plt.close()

# Plot dynamic spread
plt.figure(figsize=(12, 5))

plt.plot(
    prices.index,
    prices["Dynamic Spread"],
)

plt.title("Dynamic Spread (Kalman Filter)")
plt.xlabel("Date")
plt.ylabel("Spread")

plt.tight_layout()

plt.savefig(
    "results/figures/kalman_spread.png"
)

plt.close()

# Generate trading signals
signals = pd.DataFrame(index=prices.index)

signals["Z-Score"] = prices["Z-Score"]
signals["Signal"] = 0

signals.loc[
    signals["Z-Score"] > 2,
    "Signal",
] = -1

signals.loc[
    signals["Z-Score"] < -2,
    "Signal",
] = 1

signals.loc[
    signals["Z-Score"].abs() < 0.5,
    "Signal",
] = 0

signals["Position"] = generate_positions(
    signals["Signal"]
)

# Prepare dataframe for backtester
backtest_prices = pd.DataFrame(index=prices.index)

backtest_prices["Spread"] = prices["Dynamic Spread"]
backtest_prices["TCS"] = prices["TCS"]
backtest_prices["INFY"] = prices["INFY"]

# Use average Kalman beta for Week 7 backtest
average_beta = prices["Kalman Beta"].mean()

# Run backtest
results = backtest_strategy(
    backtest_prices,
    signals,
    average_beta,
)

trade_log = create_trade_log(results)

# Portfolio value
initial_capital = 100000

results["Portfolio Value"] = (
    initial_capital
    * (1 + results["Strategy Return"]).cumprod()
)

# Running peak
results["Running Peak"] = (
    results["Portfolio Value"].cummax()
)

# Drawdown
results["Drawdown"] = (
    results["Portfolio Value"]
    - results["Running Peak"]
) / results["Running Peak"]

# Save results
results.to_csv(
    "results/tables/kalman_backtest_summary.csv"
)

trade_log.to_csv(
    "results/tables/kalman_trade_log.csv",
    index=False,
)

# Equity curve
plt.figure(figsize=(12, 5))

plt.plot(
    results.index,
    results["Portfolio Value"],
    label="Kalman Strategy",
)

plt.title("Kalman Filter Strategy Equity Curve")
plt.xlabel("Date")
plt.ylabel("Portfolio Value (₹)")
plt.legend()

plt.tight_layout()

plt.savefig(
    "results/figures/kalman_equity_curve.png"
)

plt.close()

# Drawdown curve
plt.figure(figsize=(12, 5))

plt.fill_between(
    results.index,
    results["Drawdown"] * 100,
    0,
)

plt.title("Kalman Strategy Drawdown")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")

plt.tight_layout()

plt.savefig(
    "results/figures/kalman_drawdown.png"
)

plt.close()

# Summary
print("========== Kalman Filter Strategy ==========")

print("Average Kalman Beta:")
print(round(average_beta, 4))

print("\nFinal Portfolio Value:")
print(round(results["Portfolio Value"].iloc[-1], 2))

print("\nMaximum Drawdown:")
print(round(results["Drawdown"].min() * 100, 2), "%")

print("\nTotal Trades:")
print(len(trade_log))