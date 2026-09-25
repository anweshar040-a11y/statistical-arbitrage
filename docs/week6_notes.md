# Week 6 — Risk Metrics & Strategy Evaluation

> Project: Statistical Arbitrage — Cointegration-Based Pairs Trading with OLS Hedge Ratio

---

# Week 6 Goals

Week 6 evaluates the trading strategy using professional quantitative finance metrics.

Week 5 answered:

> "Did the strategy make or lose money?"

Week 6 answers:

> "How risky was the strategy, and was the return worth the risk?"

This is the evaluation stage of a quantitative trading project.

---

# Week 6 Deliverables

## New Files

```text
src/
└── performance_metrics.py

scripts/
└── risk_analysis.py
```

## Output Tables

```text
results/tables/
├── risk_metrics.csv
├── monthly_returns.csv
├── yearly_returns.csv
```

## Output Figures

```text
results/figures/
├── rolling_sharpe.png
├── rolling_volatility.png
├── monthly_returns_heatmap.png
├── return_distribution.png
└── underwater_curve.png
```

---

# Week 6 Project Flow

```text
Week 5 Results DataFrame
        │
        ▼
Performance Metrics
        │
        ▼
Rolling Metrics
        │
        ▼
Monthly & Yearly Returns
        │
        ▼
Risk Dashboard
```

---

# Data Used From Week 5

The `results` DataFrame from Week 5 already contains:

| Column | Purpose |
|--------|---------|
| Strategy Return | Daily percentage return. |
| Portfolio Value | Simulated portfolio value. |
| Running Peak | Highest portfolio value reached. |
| Drawdown | Percentage fall from running peak. |

Week 6 reads this dataframe and calculates additional statistics.

---

# Part 1 — Annualized Return

## Definition

Annualized return converts total return into an equivalent yearly return.

Instead of saying the portfolio lost 16.34% over several years, annualized return tells us the average yearly growth rate.

### Formula

```math
AnnualizedReturn=
\left(
\prod_{i=1}^{N}(1+r_i)
\right)^{252/N}-1
```

Where:

- `r_i` = Daily strategy return.
- `252` = Trading days in one year.
- `N` = Number of trading days.

### Interpretation

| Value | Meaning |
|-------|---------|
| Positive | Strategy grows annually. |
| Negative | Strategy shrinks annually. |

---

# Part 2 — Annualized Volatility

## Definition

Volatility measures how much daily returns fluctuate.

Higher volatility means greater uncertainty.

### Formula

```math
AnnualizedVolatility=
Std(Returns)\times\sqrt{252}
```

### Why Multiply by √252?

Daily standard deviation is converted into yearly standard deviation using:

```math
\sigma_{annual}
=
\sigma_{daily}\times\sqrt{252}
```

### Interpretation

| Volatility | Meaning |
|------------|---------|
| Low | Stable returns. |
| High | Large daily swings. |

---

# Part 3 — Sharpe Ratio

## Definition

Sharpe Ratio measures **return earned per unit of risk**.

One of the most important metrics in quantitative finance.

### Formula

```math
Sharpe=
\sqrt{252}
\times
\frac{Mean(Return)}{Std(Return)}
```

Risk-free rate is assumed to be zero in this project.

### Interpretation

| Sharpe | Meaning |
|--------|---------|
| >2 | Excellent |
| 1–2 | Good |
| 0–1 | Acceptable |
| 0 | No excess return |
| <0 | Negative risk-adjusted return |

### Why Use Sharpe?

Two strategies may earn the same return.

Sharpe tells which one achieved it with lower volatility.

---

# Part 4 — Sortino Ratio

## Definition

Sortino Ratio is similar to Sharpe but only penalizes downside volatility.

Upside volatility is ignored.

### Formula

```math
Sortino=
\sqrt{252}
\times
\frac{Mean(Return)}
{Std(Return<0)}
```

### Difference Between Sharpe and Sortino

| Sharpe | Sortino |
|--------|----------|
| Penalizes all volatility. | Penalizes only downside volatility. |
| Uses total standard deviation. | Uses downside deviation only. |

### Interpretation

Higher Sortino means better downside risk-adjusted performance.

---

# Part 5 — CAGR

## Definition

Compound Annual Growth Rate (CAGR) measures average yearly portfolio growth after compounding.

### Formula

```math
CAGR=
\left(
\frac{FinalPortfolio}
{InitialPortfolio}
\right)^{1/Years}-1
```

### Interpretation

| CAGR | Meaning |
|------|---------|
| Positive | Portfolio grows every year on average. |
| Negative | Portfolio loses value annually. |

---

# Part 6 — Calmar Ratio

## Definition

Calmar Ratio compares annual return with maximum drawdown.

### Formula

```math
Calmar=
\frac{CAGR}
{|MaximumDrawdown|}
```

### Interpretation

| Calmar | Meaning |
|--------|---------|
| >2 | Excellent risk-adjusted strategy. |
| 1–2 | Good. |
| <1 | Return is low compared to drawdown. |
| Negative | Strategy loses money relative to risk. |

---

# Part 7 — Rolling Sharpe Ratio

## Definition

Risk changes over time.

Instead of one Sharpe Ratio, calculate Sharpe over a moving window.

### Formula

```math
RollingSharpe_t=
Sharpe(Return_{t-window:t})
```

Window used:

- **60 trading days**

### Why?

Shows periods where strategy performs well or poorly.

---

# Part 8 — Rolling Volatility

## Definition

Rolling volatility measures changing market risk.

### Formula

```math
RollingVolatility=
RollingStd(Returns)\times\sqrt{252}
```

Window:

- 60 trading days.

### Interpretation

High rolling volatility means unstable strategy performance during that period.

---

# Part 9 — Monthly Returns

## Definition

Monthly return measures compounded return within each calendar month.

### Formula

```math
MonthlyReturn=
\prod(1+DailyReturns)-1
```

### Why Monthly Returns?

Professional funds evaluate consistency month by month.

Output:

```text
monthly_returns.csv
```

---

# Part 10 — Yearly Returns

## Definition

Compounded return for each calendar year.

### Formula

```math
YearlyReturn=
\prod(1+DailyReturns)-1
```

Output:

```text
yearly_returns.csv
```

Used to compare strategy performance across years.

---

# Part 11 — Return Distribution

## Definition

Histogram of daily returns.

Purpose:

- Check symmetry.
- Check frequency of gains and losses.
- Identify extreme returns.

Output:

```text
return_distribution.png
```

---

# Part 12 — Underwater Curve

## Definition

Underwater Curve visualizes drawdown over time.

Everything below zero represents portfolio decline from previous peak.

### Formula

```math
Drawdown=
\frac{Portfolio-Peak}{Peak}
```

Output:

```text
underwater_curve.png
```

---

# Risk Metrics Generated

| Metric | Purpose |
|--------|---------|
| Annualized Return | Average yearly return. |
| Annualized Volatility | Yearly risk. |
| Sharpe Ratio | Return per unit risk. |
| Sortino Ratio | Return per unit downside risk. |
| CAGR | Compound annual growth rate. |
| Calmar Ratio | CAGR divided by maximum drawdown. |

Output:

```text
risk_metrics.csv
```

---

# Week 6 Results Summary (My Project)

## Performance Summary

| Metric | Result | Interpretation |
|--------|--------|----------------|
| Initial Capital | ₹100,000 | Portfolio started with ₹100,000. |
| Final Portfolio Value | ₹83,657.50 | Portfolio ended with a loss. |
| Total Return | **-16.34%** | Overall loss during the backtest period. |
| Total Trades | **60** | Strategy completed 60 trades. |
| Winning Trades | **41** | 41 profitable trades. |
| Losing Trades | **19** | 19 losing trades. |
| Win Rate | **68.33%** | Around 2 out of every 3 trades were profitable. |
| Average Trade Return | **0.95%** | Average completed trade returned about 0.95%. |
| Maximum Drawdown | **-16.34%** | Largest portfolio decline from previous peak. |

---

## Week 6 Risk Metrics (Actual Output)

| Metric | My Result | Interpretation |
|--------|-----------|----------------|
| Annualized Return | **-3.20%** | Strategy loses about 3.2% per year on average. |
| Annualized Volatility | **0.65%** | Strategy has very low yearly volatility. |
| Sharpe Ratio | **-5.02** | Poor risk-adjusted performance because returns are consistently negative. |
| Sortino Ratio | **-3.28** | Downside-adjusted return is also negative. |
| CAGR | **-3.20%** | Portfolio shrinks by about 3.2% annually. |
| Calmar Ratio | **-0.196** | Negative return relative to maximum drawdown. |

---

# Analysis of My Results

### Positive Observations

- Trading pipeline works correctly.
- Risk metrics are calculated successfully.
- Portfolio simulation and evaluation are internally consistent.
- Monthly and yearly return reports were generated.

### Negative Observations

- Strategy is not profitable.
- Every calendar year produced a negative return.
- Sharpe and Sortino ratios are negative.
- Drawdown is relatively large compared to annual return.

### Why Did This Happen?

The strategy achieved a **68.33% win rate**, but still lost money.

Reason:

- Winning trades were generally small.
- Losing trades were much larger.
- A high win rate alone does not guarantee profitability.

This baseline result motivates improving the strategy in Week 7.

---

# What This Means for Week 7

Week 6 becomes the **baseline benchmark**.

Week 7 will replace the static OLS hedge ratio with a **Kalman Filter dynamic hedge ratio** and compare:

| OLS Hedge Ratio | Kalman Hedge Ratio |
|-----------------|--------------------|
| Static beta. | Time-varying beta. |
| One hedge ratio for all years. | Hedge ratio adapts every day. |
| Baseline metrics from Week 6. | Compare Sharpe, CAGR, Drawdown, Win Rate, Calmar. |

Goal:

Determine whether a dynamic hedge ratio improves the strategy's risk-adjusted performance.

---

# Week 6 Formula Cheat Sheet

## Annualized Return

```math
AnnualizedReturn=
\left(
\prod(1+r_i)
\right)^{252/N}-1
```

## Annualized Volatility

```math
Volatility=
Std(Return)\times\sqrt{252}
```

## Sharpe Ratio

```math
Sharpe=
\sqrt{252}
\times
\frac{Mean(Return)}{Std(Return)}
```

## Sortino Ratio

```math
Sortino=
\sqrt{252}
\times
\frac{Mean(Return)}
{Std(Return<0)}
```

## CAGR

```math
CAGR=
\left(
\frac{FinalPortfolio}
{InitialPortfolio}
\right)^{1/Years}-1
```

## Calmar Ratio

```math
Calmar=
\frac{CAGR}
{|MaximumDrawdown|}
```

## Drawdown

```math
Drawdown=
\frac{Portfolio-Peak}{Peak}
```

## Monthly Return

```math
MonthlyReturn=
\prod(1+DailyReturns)-1
```

---

# Week 6 Interview Questions

## Risk Metrics

1. What is annualized return?
2. Why annualize volatility using √252?
3. Explain Sharpe Ratio mathematically.
4. Difference between Sharpe and Sortino Ratio.
5. What does a negative Sharpe Ratio mean?

## Portfolio Evaluation

6. Explain CAGR.
7. Difference between CAGR and Total Return.
8. Explain Maximum Drawdown.
9. What is an Underwater Curve?
10. Why evaluate monthly and yearly returns separately?

## Strategy Analysis

11. Why can a strategy have a high win rate but lose money overall?
12. Why do we use rolling Sharpe instead of a single Sharpe Ratio?
13. Why is Calmar Ratio useful for trading strategies?

---

# Week 6 Completion Checklist

- [x] Create `performance_metrics.py`.
- [x] Create `risk_analysis.py`.
- [x] Calculate annualized return.
- [x] Calculate annualized volatility.
- [x] Calculate Sharpe Ratio.
- [x] Calculate Sortino Ratio.
- [x] Calculate CAGR.
- [x] Calculate Calmar Ratio.
- [x] Generate rolling Sharpe plot.
- [x] Generate rolling volatility plot.
- [x] Generate monthly returns CSV.
- [x] Generate yearly returns CSV.
- [x] Generate return distribution histogram.
- [x] Generate underwater (drawdown) curve.
- [x] Save `risk_metrics.csv`.

---

# Week 6 Key Takeaways

- Week 6 evaluates strategy quality rather than building the strategy.
- Risk-adjusted metrics are standard in quantitative finance and hedge funds.
- A profitable strategy is not enough; returns must be evaluated relative to volatility and drawdown.
- Week 6 establishes the **baseline OLS strategy benchmark** that will be compared against the **Kalman Filter strategy in Week 7**.