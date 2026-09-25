import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import load_stock
from src.hedge_ratio import calculate_hedge_ratio
from src.statistics_utils import rolling_zscore
from src.strategy import generate_positions
from src.backtester import backtest_strategy, create_trade_log
from src.performance import performance_summary

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

prices["Spread"] = prices["INFY"] - beta * prices["TCS"]
prices["Z-Score"] = rolling_zscore(prices["Spread"])

signals = pd.DataFrame(index=prices.index)

signals["Z-Score"] = prices["Z-Score"]
signals["Signal"] = 0

signals.loc[signals["Z-Score"] > 2, "Signal"] = -1
signals.loc[signals["Z-Score"] < -2, "Signal"] = 1
signals.loc[signals["Z-Score"].abs() < 0.5, "Signal"] = 0

signals["Position"] = generate_positions(signals["Signal"])

print("OLS Hedge Ratio")
print(round(beta, 4))

print("\nSignal Counts")
print(signals["Signal"].value_counts())

print("\nPosition Counts")
print(signals["Position"].value_counts())

results = backtest_strategy(
    prices,
    signals,
    beta
)

trade_log = create_trade_log(results)

trade_log.to_csv(
    "results/tables/trade_results.csv",
    index=False
)

print(trade_log.head())
print("\nTotal Trades:", len(trade_log))

initial_capital = 100000

results["Portfolio Value"] = (
    initial_capital *
    (1 + results["Strategy Return"]).cumprod()
)

results["Daily PnL"] = (
    results["Portfolio Value"].diff().fillna(0)
)

results["Cumulative Return"] = (
    results["Portfolio Value"] / initial_capital - 1
)

results.to_csv(
    "results/tables/equity_curve.csv"
)

print("\nFinal Portfolio Value:")
print(round(results["Portfolio Value"].iloc[-1], 2))

plt.figure(figsize=(12, 5))

plt.plot(
    results.index,
    results["Portfolio Value"],
    label="Portfolio"
)

plt.title("Equity Curve")
plt.xlabel("Date")
plt.ylabel("Portfolio Value (₹)")
plt.legend()

plt.tight_layout()
plt.savefig("results/figures/equity_curve.png")
plt.close()

print(
    results[results["Position"] != 0][
        ["Spread", "Spread Change", "Position", "Strategy Return"]
    ].head(20)
)

plt.figure(figsize=(12, 5))

plt.plot(results.index, results["Daily PnL"])

plt.title("Daily Profit & Loss")
plt.xlabel("Date")
plt.ylabel("PnL (₹)")

plt.tight_layout()
plt.savefig("results/figures/daily_pnl.png")
plt.close()

plt.figure(figsize=(12, 5))

plt.plot(
    results.index,
    results["Cumulative Return"] * 100
)

plt.title("Cumulative Returns")
plt.xlabel("Date")
plt.ylabel("Return (%)")

plt.tight_layout()
plt.savefig("results/figures/cumulative_returns.png")
plt.close()

results["Running Peak"] = (
    results["Portfolio Value"].cummax()
)

results["Drawdown"] = (
    results["Portfolio Value"]
    - results["Running Peak"]
) / results["Running Peak"]

plt.figure(figsize=(12, 5))

plt.plot(
    results.index,
    results["Drawdown"] * 100
)

plt.title("Drawdown Curve")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")

plt.tight_layout()
plt.savefig("results/figures/drawdown_curve.png")
plt.close()

summary = performance_summary(
    results,
    trade_log
)

summary.to_csv(
    "results/tables/performance_summary.csv",
    index=False
)

print("\nPerformance Summary")
print(summary.T)