import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import pandas as pd

from src.performance_metrics import (
    rolling_sharpe,
    rolling_volatility,
)
from src.performance_metrics import (
    annualized_return,
    annualized_volatility,
    sharpe_ratio,
    sortino_ratio,
    cagr,
    calmar_ratio,
)

results = pd.read_csv(
    "results/tables/equity_curve.csv",
    index_col="Date",
    parse_dates=True
)

results["Running Peak"] = (
    results["Portfolio Value"].cummax()
)

results["Drawdown"] = (
    results["Portfolio Value"] - results["Running Peak"]
) / results["Running Peak"]


results["Rolling Sharpe"] = rolling_sharpe(
    results["Strategy Return"]
)

results["Rolling Volatility"] = rolling_volatility(
    results["Strategy Return"]
)

#plot rolling sharpe
plt.figure(figsize=(12,5))

plt.plot(results.index, results["Rolling Sharpe"])

plt.title("Rolling Sharpe Ratio")
plt.xlabel("Date")
plt.ylabel("Sharpe")

plt.tight_layout()

plt.savefig("results/figures/rolling_sharpe.png")
plt.close()

#plot rolling volatility
plt.figure(figsize=(12,5))

plt.plot(results.index, results["Rolling Volatility"])

plt.title("Rolling Annualized Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility")

plt.tight_layout()

plt.savefig("results/figures/rolling_volatility.png")
plt.close()

#monthly and yearly returns
monthly_returns = (
    (1 + results["Strategy Return"])
    .resample("ME")
    .prod()
    - 1
)

yearly_returns = (
    (1 + results["Strategy Return"])
    .resample("YE")
    .prod()
    - 1
)

monthly_returns.to_csv(
    "results/tables/monthly_returns.csv"
)

yearly_returns.to_csv(
    "results/tables/yearly_returns.csv"
)

#monthly returns plot
plt.figure(figsize=(12,5))

monthly_returns.mul(100).plot(kind="bar")

plt.ylabel("Monthly Return (%)")

plt.tight_layout()

plt.savefig("results/figures/monthly_returns_heatmap.png")
plt.close()

#return distribution
plt.figure(figsize=(10,5))

plt.hist(
    results["Strategy Return"] * 100,
    bins=40
)

plt.title("Distribution of Daily Strategy Returns")

plt.xlabel("Daily Return (%)")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig("results/figures/return_distribution.png")
plt.close()

#underwater curve
plt.figure(figsize=(12,5))

plt.fill_between(
    results.index,
    results["Drawdown"] * 100,
    0
)

plt.title("Underwater Curve")

plt.ylabel("Drawdown (%)")

plt.tight_layout()

plt.savefig("results/figures/underwater_curve.png")
plt.close()

#metrics
metrics = {
    "Annualized Return (%)": annualized_return(
        results["Strategy Return"]
    ) * 100,

    "Annualized Volatility (%)": annualized_volatility(
        results["Strategy Return"]
    ) * 100,

    "Sharpe Ratio": sharpe_ratio(
        results["Strategy Return"]
    ),

    "Sortino Ratio": sortino_ratio(
        results["Strategy Return"]
    ),

    "CAGR (%)": cagr(results) * 100,

    "Calmar Ratio": calmar_ratio(results),
}

metrics_df = pd.DataFrame(
    metrics,
    index=[0]
)

metrics_df.to_csv(
    "results/tables/risk_metrics.csv",
    index=False
)

print(metrics_df.T)