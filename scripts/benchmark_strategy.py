import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import pandas as pd

from src.data_loader import load_stock
from src.benchmark import buy_and_hold_portfolio
from src.performance_metrics import (
    sharpe_ratio,
    annualized_return,
    annualized_volatility,
    cagr,
    calmar_ratio,
)

# Load strategy results
strategy = pd.read_csv(
    "results/tables/equity_curve.csv",
    index_col="Date",
    parse_dates=True,
)

# Load stock prices
tcs = load_stock("TCS.NS")
infy = load_stock("INFY.NS")

prices = pd.concat(
    [tcs["Close"], infy["Close"]],
    axis=1,
).dropna()

prices.columns = ["TCS", "INFY"]

prices = prices.loc[strategy.index]

benchmark = buy_and_hold_portfolio(prices)

benchmark.to_csv(
    "results/tables/benchmark_equity_curve.csv"
)

# Portfolio comparison
plt.figure(figsize=(12,5))

plt.plot(
    strategy.index,
    strategy["Portfolio Value"],
    label="Statistical Arbitrage",
    linewidth=2,
)

plt.plot(
    benchmark.index,
    benchmark["Portfolio Value"],
    label="Buy & Hold",
    linewidth=2,
)

plt.title("Statistical Arbitrage vs Buy & Hold")

plt.xlabel("Date")

plt.ylabel("Portfolio Value (₹)")

plt.legend()

plt.tight_layout()

plt.savefig(
    "results/figures/benchmark_equity_curve.png"
)

plt.close()

# Cumulative return comparison
strategy["Cumulative Return"] = (
    strategy["Portfolio Value"] / 100000 - 1
)

benchmark["Cumulative Return"] = (
    benchmark["Portfolio Value"] / 100000 - 1
)

plt.figure(figsize=(12,5))

plt.plot(
    strategy.index,
    strategy["Cumulative Return"] * 100,
    label="Strategy",
)

plt.plot(
    benchmark.index,
    benchmark["Cumulative Return"] * 100,
    label="Buy & Hold",
)

plt.title("Cumulative Return Comparison")

plt.ylabel("Return (%)")

plt.legend()

plt.tight_layout()

plt.savefig(
    "results/figures/cumulative_return_comparison.png"
)

plt.close()

# Drawdown comparison
strategy["Running Peak"] = (
    strategy["Portfolio Value"].cummax()
)

strategy["Drawdown"] = (
    strategy["Portfolio Value"]
    - strategy["Running Peak"]
) / strategy["Running Peak"]

plt.figure(figsize=(12,5))

plt.plot(
    strategy.index,
    strategy["Drawdown"] * 100,
    label="Strategy",
)

plt.plot(
    benchmark.index,
    benchmark["Drawdown"] * 100,
    label="Buy & Hold",
)

plt.title("Drawdown Comparison")

plt.ylabel("Drawdown (%)")

plt.legend()

plt.tight_layout()

plt.savefig(
    "results/figures/benchmark_drawdown.png"
)

plt.close()

# Return distribution
plt.figure(figsize=(10,5))

plt.hist(
    strategy["Strategy Return"] * 100,
    bins=40,
    alpha=0.6,
    label="Strategy",
)

plt.hist(
    benchmark["Benchmark Return"] * 100,
    bins=40,
    alpha=0.6,
    label="Buy & Hold",
)

plt.title("Daily Return Distribution")

plt.xlabel("Daily Return (%)")

plt.ylabel("Frequency")

plt.legend()

plt.tight_layout()

plt.savefig(
    "results/figures/benchmark_return_distribution.png"
)

plt.close()

# Performance summary
summary = pd.DataFrame({
    "Metric":[
        "Final Portfolio Value",
        "Annualized Return",
        "Annualized Volatility",
        "Sharpe Ratio",
        "CAGR",
        "Maximum Drawdown",
        "Calmar Ratio",
    ],

    "Strategy":[
        strategy["Portfolio Value"].iloc[-1],
        annualized_return(strategy["Strategy Return"]),
        annualized_volatility(strategy["Strategy Return"]),
        sharpe_ratio(strategy["Strategy Return"]),
        cagr(strategy),
        abs(strategy["Drawdown"].min()),
        calmar_ratio(strategy),
    ],

    "Buy & Hold":[
        benchmark["Portfolio Value"].iloc[-1],
        annualized_return(benchmark["Benchmark Return"]),
        annualized_volatility(benchmark["Benchmark Return"]),
        sharpe_ratio(benchmark["Benchmark Return"]),
        cagr(benchmark),
        abs(benchmark["Drawdown"].min()),
        calmar_ratio(benchmark),
    ]
})

summary.to_csv(
    "results/tables/benchmark_summary.csv",
    index=False,
)

print("\nStrategy vs Buy & Hold\n")
print(summary)