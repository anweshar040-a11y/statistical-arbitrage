# 📈 Statistical Arbitrage Trading Strategy using Cointegration & Kalman Filter

> End-to-end quantitative trading research project implementing a **cointegration-based pairs trading strategy** with **dynamic Kalman Filter hedge ratios**, **walk-forward validation**, **parameter optimization**, **risk analytics**, and an interactive **Streamlit dashboard**.

---

## 🚀 Project Highlights

* Cointegration-based statistical arbitrage on **TCS** and **Infosys**.
* Augmented Dickey-Fuller (ADF) stationarity testing.
* Engle-Granger cointegration testing.
* OLS hedge ratio estimation.
* Kalman Filter dynamic hedge ratio.
* Rolling Z-score mean-reversion trading signals.
* Custom backtesting engine with transaction costs.
* Sharpe, Sortino, CAGR, Calmar, and Drawdown analysis.
* Walk-forward out-of-sample validation.
* Parameter optimization with grid search.
* Buy & Hold benchmark comparison.
* Interactive Streamlit + Plotly dashboard.

## Project Pipeline

![Project Pipeline](results/figures/project_pipeline.png)

## 📊 Interactive Dashboard

### Portfolio Overview

![Dashboard Overview](results/figures/dashboard_overview.png)

### Equity Curve

![Equity Curve](results/figures/dashboard_equity_curve.png)

### Drawdown Analysis

![Drawdown](results/figures/dashboard_drawdown.png)

### Kalman vs OLS Strategy Comparison

![Kalman](results/figures/dashboard_kalman.png)

### Parameter Optimization Heatmap

![Heatmap](results/figures/dashboard_heatmap.png)

## 📈 Results

### 📊 Strategy Equity Curve

![Strategy Equity Curve](results/figures/equity_curve.png)

### 📈 Rolling Z-Score Signals

![Rolling Z-Score Signals](results/figures/rolling_zscore.png)

### 🔄 Spread Trading Signals

![Spread Trading Signals](results/figures/spread_signals.png)

### 📉 Drawdown Curve

![Drawdown Curve](results/figures/drawdown_curve.png)

### 🧠 Dynamic Kalman Hedge Ratio

![Dynamic Kalman Hedge Ratio](results/figures/kalman_beta.png)

### ⚖️ OLS vs Kalman Equity Curve

![OLS vs Kalman Equity Curve](results/figures/ols_vs_kalman_equity_curve.png)
## 📋 Performance Summary

### OLS Strategy

| Metric                |     Result |
| --------------------- | ---------: |
| Final Portfolio Value | ₹98,775.17 |
| Annualized Return     |     -0.22% |
| Annualized Volatility |      3.75% |
| Sharpe Ratio          |     -0.041 |
| Maximum Drawdown      |  **8.76%** |
| Total Trades          |         60 |

### Kalman Filter Strategy

| Metric                |     Result |
| --------------------- | ---------: |
| Average Kalman Beta   |     0.4553 |
| Final Portfolio Value | ₹94,278.23 |
| Maximum Drawdown      |  **5.72%** |
| Total Trades          |         59 |

### Walk-Forward Validation

| Metric                |          Result |
| --------------------- | --------------: |
| Testing Window        |            2024 |
| Sharpe Ratio          |      **1.3647** |
| Final Portfolio Value | **₹104,261.52** |
| Maximum Drawdown      |       **1.24%** |
| Trades                |              17 |

### Benchmark Comparison

| Metric                |   Strategy |  Buy & Hold |
| --------------------- | ---------: | ----------: |
| Final Portfolio Value | ₹98,775.17 | ₹101,009.84 |
| Maximum Drawdown      |  **8.76%** |      50.18% |
| Annualized Volatility |  **3.75%** |      22.05% |
| Sharpe Ratio          |     -0.041 |       0.119 |

## 🛠️ Technologies Used

| Category         | Tools                             |
| ---------------- | --------------------------------- |
| Programming      | Python                            |
| Data Analysis    | Pandas, NumPy                     |
| Statistics       | Statsmodels                       |
| Machine Learning | Scikit-Learn                      |
| Time Series      | Kalman Filter, Rolling Statistics |
| Visualization    | Matplotlib, Plotly                |
| Dashboard        | Streamlit                         |
| Version Control  | Git, GitHub                       |

## 📁 Repository Structure

```text
statistical-arbitrage/

├── dashboard/
├── data/
├── results/
│   ├── figures/
│   └── tables/
├── scripts/
├── src/
├── README.md
├── requirements.txt
└── LICENSE
```
