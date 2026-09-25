import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import pandas as pd

ols = pd.read_csv(
    "results/tables/equity_curve.csv",
    index_col="Date",
    parse_dates=True,
)

kalman = pd.read_csv(
    "results/tables/kalman_backtest_summary.csv",
    index_col="Date",
    parse_dates=True,
)

beta = pd.read_csv(
    "results/tables/kalman_beta.csv",
    index_col="Date",
    parse_dates=True,
)

# add drawdown columns if they are missing
if "Drawdown" not in ols.columns:
    ols["Running Peak"] = ols["Portfolio Value"].cummax()
    ols["Drawdown"] = (
        ols["Portfolio Value"] - ols["Running Peak"]
    ) / ols["Running Peak"]

if "Drawdown" not in kalman.columns:
    kalman["Running Peak"] = kalman["Portfolio Value"].cummax()
    kalman["Drawdown"] = (
        kalman["Portfolio Value"] - kalman["Running Peak"]
    ) / kalman["Running Peak"]

plt.figure(figsize=(12,5))

plt.plot(
    ols.index,
    ols["Portfolio Value"],
    label="OLS Strategy",
)

plt.plot(
    kalman.index,
    kalman["Portfolio Value"],
    label="Kalman Strategy",
)

plt.legend()

plt.title("OLS vs Kalman Equity Curve")

plt.tight_layout()

plt.savefig(
    "results/figures/ols_vs_kalman_equity_curve.png"
)

plt.close()

#plot hedge ratio difference
plt.figure(figsize=(12,5))

plt.plot(
    beta.index,
    beta["Kalman Beta"],
    label="Kalman Beta",
)

plt.axhline(
    beta["Kalman Beta"].mean(),
    linestyle="--",
    label="Average Beta",
)

plt.legend()

plt.title("Dynamic Hedge Ratio Through Time")

plt.tight_layout()

plt.savefig(
    "results/figures/hedge_ratio_difference.png"
)

plt.close()

#compare risk metrics
from src.performance_metrics import (
    annualized_return,
    annualized_volatility,
    sharpe_ratio,
    sortino_ratio,
    cagr,
    calmar_ratio,
)

comparison = pd.DataFrame({
    "Metric":[
        "Annualized Return",
        "Annualized Volatility",
        "Sharpe Ratio",
        "Sortino Ratio",
        "CAGR",
        "Maximum Drawdown",
        "Calmar Ratio",
    ],

    "OLS":[
        annualized_return(ols["Strategy Return"]),
        annualized_volatility(ols["Strategy Return"]),
        sharpe_ratio(ols["Strategy Return"]),
        sortino_ratio(ols["Strategy Return"]),
        cagr(ols),
        abs(ols["Drawdown"].min()),
        calmar_ratio(ols),
    ],

    "Kalman":[
        annualized_return(kalman["Strategy Return"]),
        annualized_volatility(kalman["Strategy Return"]),
        sharpe_ratio(kalman["Strategy Return"]),
        sortino_ratio(kalman["Strategy Return"]),
        cagr(kalman),
        abs(kalman["Drawdown"].min()),
        calmar_ratio(kalman),
    ],
})

comparison.to_csv(
    "results/tables/comparison_metrics.csv",
    index=False,
)

print(comparison)