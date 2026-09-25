# Week 7 — Kalman Filter Dynamic Hedge Ratio

> Project: Statistical Arbitrage — Cointegration-Based Pairs Trading with Dynamic Hedge Ratio

---

# Week 7 Goals

Week 7 upgrades the statistical arbitrage strategy by replacing the **static Ordinary Least Squares (OLS) hedge ratio** with a **Kalman Filter dynamic hedge ratio**.

The objective is to allow the hedge ratio to **adapt over time** instead of remaining constant throughout the entire dataset.

This is the research-focused week of the project and introduces a state-space model commonly used in quantitative finance.

---

# Week 7 Deliverables

## New Files

```text
src/
├── kalman_filter.py
└── dynamic_spread.py

scripts/
├── kalman_analysis.py
└── compare_hedge_ratios.py
```

## Output Tables

```text
results/tables/
├── kalman_beta.csv
├── kalman_backtest_summary.csv
├── kalman_trade_log.csv
└── comparison_metrics.csv
```

## Output Figures

```text
results/figures/
├── kalman_beta.png
├── kalman_spread.png
├── ols_vs_kalman_equity_curve.png
└── hedge_ratio_difference.png
```

---

# Week 7 Project Flow

```text
Week 6 OLS Strategy
        │
        ▼
Kalman Filter estimates Dynamic Beta
        │
        ▼
Dynamic Spread
        │
        ▼
Rolling Z-Score
        │
        ▼
Trading Signals
        │
        ▼
Backtesting
        │
        ▼
Compare OLS vs Kalman
```

---

# Why Replace OLS?

## Static Hedge Ratio (Week 3–6)

The spread was calculated as:

```math
Spread = INFY - \beta \times TCS
```

Where **β** was estimated once using OLS regression.

### Limitation

The relationship between TCS and INFY changes over time because market conditions, earnings, sector movements, and volatility change.

A single hedge ratio cannot capture these changes.

---

## Dynamic Hedge Ratio (Week 7)

Instead of one constant beta:

| Date | Hedge Ratio |
|------|-------------|
| Jan 2021 | 1.31 |
| Jul 2021 | 1.37 |
| Jan 2022 | 1.29 |
| Apr 2024 | 1.48 |
| Jan 2026 | 1.35 |

The Kalman Filter estimates a **new hedge ratio every trading day**.

---

# Kalman Filter Theory

## What is a Kalman Filter?

A Kalman Filter is a recursive Bayesian estimation algorithm that continuously updates an unknown variable as new observations arrive.

In this project:

| Hidden State | Observation |
|--------------|-------------|
| Hedge Ratio (β) | Daily stock prices |

The hedge ratio is not directly observable.

The Kalman Filter estimates it using historical information and today's prices.

---

## Two Steps of the Kalman Filter

### 1. Prediction Step

Estimate today's beta using yesterday's beta.

```math
\beta_t^- = \beta_{t-1}
```

### 2. Update Step

Observe today's prices.

Correct the estimate.

```math
\beta_t = \beta_t^- + K_t \times Error_t
```

Where:

- **K** = Kalman Gain.
- **Error** = Difference between predicted and observed prices.

---

# State Space Model

## State Equation

```math
\beta_t = \beta_{t-1} + w_t
```

The hedge ratio evolves gradually over time.

## Observation Equation

```math
INFY_t = \beta_t \times TCS_t + v_t
```

Today's observed INFY price depends on today's hedge ratio.

---

# Why Kalman Filter Instead of Rolling Regression?

| Rolling Regression | Kalman Filter |
|--------------------|--------------|
| Uses fixed rolling window. | Uses all previous observations recursively. |
| Hedge ratio changes abruptly every window. | Hedge ratio changes smoothly over time. |
| Less adaptive. | More adaptive to market changes. |

---

# Dynamic Spread

After estimating daily beta:

```math
Spread_t = INFY_t - \beta_t \times TCS_t
```

Unlike Week 3, the spread now changes because both stock prices **and** beta change.

---

# Trading Strategy

The trading rules remain unchanged.

## Entry Rules

| Condition | Action |
|-----------|--------|
| Z-score > 2 | Short Spread |
| Z-score < -2 | Long Spread |

## Exit Rule

| Condition | Action |
|-----------|--------|
| |Z-score| < 0.5 | Exit Position |

This allows a fair comparison between OLS and Kalman.

---

# Backtesting Process

The Week 5 backtester is reused.

The Kalman strategy follows the same pipeline:

1. Calculate dynamic spread.
2. Calculate rolling Z-score.
3. Generate signals.
4. Generate positions.
5. Calculate strategy returns.
6. Simulate portfolio value.
7. Calculate drawdown.

This ensures both strategies are evaluated under identical assumptions.

---

# Figures Generated

| Figure | Purpose |
|--------|---------|
| `kalman_beta.png` | Daily hedge ratio estimated by the Kalman Filter. |
| `kalman_spread.png` | Dynamic spread between TCS and INFY. |
| `ols_vs_kalman_equity_curve.png` | Portfolio value comparison between OLS and Kalman strategies. |
| `hedge_ratio_difference.png` | Dynamic beta compared with its average value. |

---

# Tables Generated

| Table | Purpose |
|-------|---------|
| `kalman_beta.csv` | Daily hedge ratio and spread values. |
| `kalman_backtest_summary.csv` | Portfolio values and returns for Kalman strategy. |
| `kalman_trade_log.csv` | Completed Kalman trades. |
| `comparison_metrics.csv` | Side-by-side comparison of OLS and Kalman metrics. |

---

# Week 7 Results Summary

The Kalman Filter was introduced to estimate a **dynamic hedge ratio** instead of using a single OLS hedge ratio across the entire dataset.

## OLS vs Kalman Comparison

| Metric | OLS Strategy | Kalman Strategy |
|--------|--------------|-----------------|
| Annualized Return | **-3.20%** | **-3.18%** |
| Annualized Volatility | **0.647%** | **0.666%** |
| Sharpe Ratio | **-5.02** | **-4.85** |
| Sortino Ratio | **-3.28** | **-10.54** |
| CAGR | **-3.20%** | **-3.18%** |
| Maximum Drawdown | **16.34%** | **16.23%** |
| Calmar Ratio | **-0.1959** | **-0.1958** |

---

## Observations

- Annualized Return improved slightly from **-3.20%** to **-3.18%**.
- Sharpe Ratio improved from **-5.02** to **-4.85**, indicating a modest improvement in risk-adjusted performance.
- Maximum Drawdown decreased from **16.34%** to **16.23%**, suggesting slightly better capital preservation.
- CAGR improved marginally.
- Annualized Volatility increased slightly, showing the strategy became a little more responsive.
- Sortino Ratio became more negative, indicating worse downside-adjusted performance despite improvements in other metrics.

---

## Interpretation of the Results

### Positive Findings

- The Kalman Filter successfully produced a time-varying hedge ratio.
- Dynamic beta adapted to changing price relationships between TCS and INFY.
- The strategy showed small improvements in return, Sharpe Ratio, CAGR, and drawdown.
- The comparison framework between OLS and Kalman is now established.

### Negative Findings

- The strategy remained unprofitable overall.
- Improvements were relatively small.
- Downside-adjusted performance (Sortino Ratio) deteriorated, suggesting losing trades became more concentrated.

---

## Conclusion

The Kalman Filter produced a more adaptive hedge ratio and improved several overall performance metrics, but it did not fully solve the profitability problem. This establishes the Kalman strategy as an improved but still imperfect model, motivating further optimization through walk-forward testing, parameter tuning, and improved trade management in Week 8.

The OLS strategy is retained as the **baseline benchmark**, while the Kalman strategy becomes the **dynamic benchmark** for future improvements.

---

# What Changes in Week 8?

Week 8 focuses on improving the trading strategy rather than the hedge ratio.

Planned improvements include:

- Dollar-neutral position sizing.
- Walk-forward (out-of-sample) testing.
- Parameter optimization for Z-score thresholds.
- Stop-loss and maximum holding period.
- Comparison against Buy & Hold benchmarks.
- Final performance dashboard and strategy evaluation.

Week 8 aims to determine whether these improvements produce a more robust statistical arbitrage strategy than both the OLS and Kalman versions.

---

# Week 7 Formula Cheat Sheet

## Static Spread (OLS)

```math
Spread = INFY - \beta \times TCS
```

## Dynamic Spread (Kalman)

```math
Spread_t = INFY_t - \beta_t \times TCS_t
```

## Prediction Step

```math
\beta_t^- = \beta_{t-1}
```

## Update Step

```math
\beta_t = \beta_t^- + K_t \times Error_t
```

## State Equation

```math
\beta_t = \beta_{t-1} + w_t
```

## Observation Equation

```math
INFY_t = \beta_t \times TCS_t + v_t
```

---

# Week 7 Interview Questions

### Kalman Filter

1. What problem does the Kalman Filter solve in pairs trading?
2. Why is a static hedge ratio insufficient?
3. Explain the prediction and update steps of the Kalman Filter.
4. What is a hidden state in a state-space model?
5. What is Kalman Gain?

### Trading Strategy

6. How is the dynamic spread calculated?
7. Why were the entry and exit rules kept unchanged when comparing OLS and Kalman?
8. How do you compare two trading strategies fairly?

### Results Analysis

9. Why did Sharpe Ratio improve while Sortino Ratio became worse?
10. Why can a strategy improve several risk metrics and still remain unprofitable?

---

# Week 7 Completion Checklist

- [x] Implement Kalman Filter dynamic hedge ratio.
- [x] Generate daily hedge ratio for every trading day.
- [x] Calculate dynamic spread.
- [x] Generate rolling Z-score using dynamic spread.
- [x] Backtest Kalman strategy.
- [x] Generate Kalman trade log.
- [x] Generate Kalman portfolio equity curve.
- [x] Compare OLS and Kalman performance metrics.
- [x] Generate comparison figures.
- [x] Establish Kalman strategy as the Week 7 benchmark for Week 8 optimization.

---

# Week 7 Key Takeaways

- Introduced a **dynamic hedge ratio** using a Kalman Filter instead of a static OLS estimate.
- Built a second complete trading strategy using the same signal-generation and backtesting pipeline.
- Compared OLS and Kalman strategies using identical risk metrics.
- Observed modest improvements in return, Sharpe Ratio, CAGR, and drawdown, while identifying weaker downside-adjusted performance through the Sortino Ratio.
- Established a research baseline for optimizing the strategy in Week 8.