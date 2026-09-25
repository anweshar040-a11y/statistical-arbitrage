import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import load_stock
from src.hedge_ratio import calculate_hedge_ratio
from src.optimizer import run_strategy

tcs = load_stock("TCS.NS")
infy = load_stock("INFY.NS")

prices = pd.concat(
    [tcs["Close"], infy["Close"]],
    axis=1,
).dropna()

prices.columns = ["TCS", "INFY"]

alpha, beta, model = calculate_hedge_ratio(
    prices["TCS"],
    prices["INFY"],
)

prices["Spread"] = (
    prices["INFY"]
    - beta * prices["TCS"]
)

ENTRY_VALUES = [1.8, 2.0, 2.2, 2.5]
EXIT_VALUES = [0.2, 0.5, 0.8, 1.0]

results_table = []

best_results = None
best_sharpe = float("-inf")

for entry in ENTRY_VALUES:

    for exit in EXIT_VALUES:

        metrics, portfolio = run_strategy(
            prices,
            beta,
            entry,
            exit,
        )

        results_table.append(metrics)

        if metrics["Sharpe"] > best_sharpe:

            best_sharpe = metrics["Sharpe"]
            best_results = portfolio.copy()
            best_metrics = metrics.copy()

optimization_df = pd.DataFrame(results_table)

optimization_df = optimization_df.sort_values(
    "Sharpe",
    ascending=False,
)

optimization_df.to_csv(
    "results/tables/optimization_results.csv",
    index=False,
)
heatmap = optimization_df.pivot(
    index="Entry Z",
    columns="Exit Z",
    values="Sharpe",
)

plt.figure(figsize=(7,6))

plt.imshow(
    heatmap,
    aspect="auto",
)

plt.xticks(
    range(len(heatmap.columns)),
    heatmap.columns,
)

plt.yticks(
    range(len(heatmap.index)),
    heatmap.index,
)

plt.colorbar(label="Sharpe Ratio")

plt.title("Sharpe Ratio Heatmap")

plt.xlabel("Exit Threshold")
plt.ylabel("Entry Threshold")

plt.tight_layout()

plt.savefig(
    "results/figures/sharpe_heatmap.png"
)

plt.close()

pd.DataFrame([best_metrics]).to_csv(
    "results/tables/best_parameters.csv",
    index=False,
)

print("Best Parameters")
print(pd.DataFrame([best_metrics]).T)

plt.figure(figsize=(12,5))

plt.plot(
    best_results.index,
    best_results["Portfolio Value"],
)

plt.title("Best Optimized Portfolio")
plt.xlabel("Date")
plt.ylabel("Portfolio Value (₹)")

plt.tight_layout()

plt.savefig(
    "results/figures/portfolio_comparison_best.png"
)

plt.close()