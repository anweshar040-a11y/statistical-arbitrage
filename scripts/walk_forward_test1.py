import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import load_stock
from src.walk_forward1 import walk_forward_window

tcs = load_stock("TCS.NS")
infy = load_stock("INFY.NS")

prices = pd.concat(
    [tcs["Close"], infy["Close"]],
    axis=1,
).dropna()

prices.columns = ["TCS", "INFY"]

prices = prices.loc["2021":"2026"]

walk_results = []

portfolio_results = []

windows = [
    ("2023-12-31", "2024"),
    ("2024-12-31", "2025"),
    ("2025-12-31", "2026"),
]

for train_end, test_year in windows:

    train = prices.loc[:train_end]

    test = prices.loc[test_year]

    metrics, results = walk_forward_window(
        train,
        test,
    )

    walk_results.append(metrics)

    results["Test Year"] = test_year

    portfolio_results.append(results)

summary = pd.DataFrame(walk_results)

summary.to_csv(
    "results/tables/walk_forward_summary.csv",
    index=False,
)

combined = pd.concat(portfolio_results)

combined.to_csv(
    "results/tables/walk_forward_portfolios.csv",
)

print(summary)

plt.figure(figsize=(12,5))

for year in combined["Test Year"].unique():

    yearly = combined[
        combined["Test Year"] == year
    ]

    plt.plot(
        yearly.index,
        yearly["Portfolio Value"],
        label=year,
    )

plt.title("Walk-Forward Portfolio Performance")

plt.xlabel("Date")

plt.ylabel("Portfolio Value (₹)")

plt.legend()

plt.tight_layout()

plt.savefig(
    "results/figures/walk_forward_equity_curve.png"
)

plt.close()

plt.figure(figsize=(8,5))

plt.bar(
    summary["Test Start"].astype(str),
    summary["Sharpe"],
)

plt.title("Walk-Forward Sharpe Ratio")

plt.xlabel("Testing Window")

plt.ylabel("Sharpe Ratio")

plt.tight_layout()

plt.savefig(
    "results/figures/walk_forward_sharpe.png"
)

plt.close()

plt.figure(figsize=(8,5))

plt.bar(
    summary["Test Start"].astype(str),
    summary["Drawdown"] * 100,
)

plt.title("Walk-Forward Maximum Drawdown")

plt.xlabel("Testing Window")

plt.ylabel("Drawdown (%)")

plt.tight_layout()

plt.savefig(
    "results/figures/walk_forward_drawdown.png"
)

plt.close()

best_window = summary.sort_values(
    "Sharpe",
    ascending=False,
).iloc[0]

print("\nBest Testing Window")

print(best_window)