import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import pandas as pd

from src.data_loader import load_stock
from src.hedge_ratio import calculate_hedge_ratio
from src.statistics_utils import rolling_zscore
from src.strategy_risk_managed import generate_positions_risk_managed
from src.backtester import backtest_strategy, create_trade_log


# Load stock prices
tcs = load_stock("TCS.NS")
infy = load_stock("INFY.NS")

prices = pd.concat(
    [tcs["Close"], infy["Close"]],
    axis=1
).dropna()

prices.columns = ["TCS", "INFY"]


# Calculate hedge ratio
alpha, beta, model = calculate_hedge_ratio(
    prices["TCS"],
    prices["INFY"]
)

print(f"OLS Hedge Ratio: {beta:.4f}")


# Calculate spread
prices["Spread"] = (
    prices["INFY"]
    - beta * prices["TCS"]
)


# Rolling Z-score
prices["Z-Score"] = rolling_zscore(
    prices["Spread"]
)


# Generate signals
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


# Risk-managed positions
signals["Position"] = generate_positions_risk_managed(
    signals["Signal"],
    prices["Z-Score"],
    stop_loss=3.5,
    take_profit=0.5,
    max_holding_days=20
)


# Backtest
results = backtest_strategy(
    prices,
    signals,
    beta
)


# Portfolio value
initial_capital = 100000

results["Portfolio Value"] = (
    initial_capital *
    (1 + results["Strategy Return"]).cumprod()
)


# Drawdown
results["Running Peak"] = (
    results["Portfolio Value"].cummax()
)

results["Drawdown"] = (
    results["Portfolio Value"]
    - results["Running Peak"]
) / results["Running Peak"]


# Trade log
trade_log = create_trade_log(results)


# Save tables
results.to_csv(
    "results/tables/risk_managed_equity_curve.csv"
)

trade_log.to_csv(
    "results/tables/risk_managed_trade_log.csv",
    index=False
)


# Equity curve
plt.figure(figsize=(12, 5))

plt.plot(
    results.index,
    results["Portfolio Value"],
    label="Risk Managed Strategy"
)

plt.title("Risk Managed Equity Curve")
plt.xlabel("Date")
plt.ylabel("Portfolio Value (₹)")
plt.legend()

plt.tight_layout()

plt.savefig(
    "results/figures/risk_managed_equity_curve.png"
)

plt.close()


# Drawdown curve
plt.figure(figsize=(12, 5))

plt.fill_between(
    results.index,
    results["Drawdown"] * 100,
    0
)

plt.title("Risk Managed Drawdown")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")

plt.tight_layout()

plt.savefig(
    "results/figures/risk_managed_drawdown.png"
)

plt.close()


# Trade duration
trade_log["Holding Days"] = (
    pd.to_datetime(trade_log["Exit Date"])
    - pd.to_datetime(trade_log["Entry Date"])
).dt.days

plt.figure(figsize=(10, 5))

plt.hist(
    trade_log["Holding Days"],
    bins=15
)

plt.title("Distribution of Holding Periods")
plt.xlabel("Holding Days")
plt.ylabel("Number of Trades")

plt.tight_layout()

plt.savefig(
    "results/figures/holding_period_distribution.png"
)

plt.close()


# Summary
print("\n========== Risk Managed Strategy ==========")

print("Final Portfolio Value:")
print(round(results["Portfolio Value"].iloc[-1], 2))

print("\nMaximum Drawdown:")
print(round(results["Drawdown"].min() * 100, 2), "%")

print("\nTotal Trades:")
print(len(trade_log))

print("\nAverage Holding Days:")
print(round(trade_log["Holding Days"].mean(), 2))

print("\nWinning Trades:")
print((trade_log["Return"] > 0).sum())

print("\nLosing Trades:")
print((trade_log["Return"] <= 0).sum())

print("\nWin Rate:")
print(
    round(
        (trade_log["Return"] > 0).mean() * 100,
        2
    ),
    "%"
)