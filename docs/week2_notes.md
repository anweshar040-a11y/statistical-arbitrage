# Week 2 Notes — Stationarity & Augmented Dickey-Fuller (ADF) Test

## Project Context

**Project:** Statistical Arbitrage — Cointegration-Based Pairs Trading with a Kalman Filter Hedge Ratio

### Goal of Week 2

Learn how to determine whether a time series is **stationary**, because stationarity is the statistical foundation of pairs trading and cointegration.

---

# 1. What is Stationarity?

A time series is **stationary** if its statistical properties remain constant over time.

A stationary series has three important properties:

* **Constant Mean** — The average value stays roughly the same over time.
* **Constant Variance** — The spread (volatility) does not systematically increase or decrease.
* **Constant Covariance** — The relationship between observations depends only on the time lag, not on when the observations occur.

### Intuition

* Stationary data fluctuates around a stable average.
* Non-stationary data drifts upward or downward and does not return to a fixed average.

### Why Stationarity Matters

Pairs trading assumes the **spread between two stocks** is mean-reverting.

Mean reversion only makes sense if the spread is stationary.

---

# 2. Stock Prices vs Returns

## Stock Prices

* Represent the market value of a stock.
* Usually trend upward or downward over long periods.
* Generally **non-stationary**.

## Daily Returns

Daily return measures the percentage change in price from one trading day to the next.

Formula:

**Daily Return**

Rₜ = (Pₜ − Pₜ₋₁) / Pₜ₋₁

Where:

* Pₜ = Today's closing price.
* Pₜ₋₁ = Yesterday's closing price.

### Why Returns Are Preferred

Returns remove much of the long-term trend present in prices.

In finance, returns are often stationary even when prices are not.

---

# 3. Random Walk

A random walk is a common mathematical model for stock prices.

Equation:

Pₜ = Pₜ₋₁ + εₜ

Where εₜ is a random shock.

### Interpretation

* Today's price equals yesterday's price plus a random movement.
* Random shocks accumulate over time.
* The series "wanders" without returning to a fixed mean.

### Characteristics

* Mean changes over time.
* Variance grows over time.
* Prices are typically non-stationary.

---

# 4. Unit Root

A unit root indicates a non-stationary process.

General equation:

Yₜ = ρYₜ₋₁ + εₜ

Interpretation of ρ:

* ρ = 1 → Unit root (Random Walk).
* |ρ| less than 1 → Stationary process.
* |ρ| greater than 1 → Explosive process.

### Why We Care

The ADF test checks whether a series contains a unit root.

---

# 5. Augmented Dickey-Fuller (ADF) Test

The ADF test is a statistical test used to determine whether a time series is stationary.

## Null Hypothesis (H₀)

The series contains a **unit root**.

Meaning: The series is **non-stationary**.

## Alternative Hypothesis (H₁)

The series **does not contain** a unit root.

Meaning: The series is **stationary**.

---

# 6. Understanding ADF Output

The `adfuller()` function returns several values.

| Output          | Meaning                                            |
| --------------- | -------------------------------------------------- |
| ADF Statistic   | Test statistic computed by the test.               |
| p-value         | Probability used for hypothesis testing.           |
| Lags Used       | Number of lagged differences used.                 |
| Observations    | Number of observations after lagging.              |
| Critical Values | Thresholds at 1%, 5%, and 10% significance levels. |

Example:

| Output        | Value |
| ------------- | ----: |
| ADF Statistic | -4.20 |
| p-value       | 0.001 |
| Lags Used     |     3 |
| Observations  |  1380 |

Critical Values:

| Significance Level | Critical Value |
| ------------------ | -------------: |
| 1%                 |          -3.50 |
| 5%                 |          -2.89 |
| 10%                |          -2.58 |

---

# 7. How to Interpret the ADF Statistic

The ADF statistic is compared with the critical values.

### Example

ADF Statistic = -4.20

Critical Value (5%) = -2.89

Since:

-4.20 is less than -2.89

The statistic is more negative than the critical value.

### Decision

Reject the null hypothesis.

**Conclusion:** The series is stationary.

---

# 8. How to Interpret the p-value

Decision Rule:

| p-value                               | Decision                           |
| ------------------------------------- | ---------------------------------- |
| p-value less than 0.05                | Reject H₀ → Stationary.            |
| p-value greater than or equal to 0.05 | Cannot reject H₀ → Non-stationary. |

### Example 1

p-value = 0.45

Conclusion:

* Cannot reject the null hypothesis.
* Series is non-stationary.

### Example 2

p-value = 0.0000

Conclusion:

* Reject the null hypothesis.
* Series is stationary.

---

# 9. Results from the Project

### TCS Closing Price

* ADF Statistic ≈ -1.65
* p-value ≈ 0.456

Conclusion:

TCS closing prices are **non-stationary**.

### TCS Daily Returns

* ADF Statistic ≈ -36.97
* p-value = 0.0000

Conclusion:

TCS daily returns are **stationary**.

### Important Observation

Prices failed the ADF test.

Returns passed the ADF test.

This confirms a common property of financial markets.

---

# 10. Testing Multiple Stocks

The project tested multiple NIFTY stocks using the same reusable function.

Stocks tested:

* RELIANCE.NS
* TCS.NS
* INFY.NS
* HDFCBANK.NS
* ICICIBANK.NS
* SBIN.NS
* ITC.NS
* LT.NS
* BHARTIARTL.NS
* KOTAKBANK.NS

For each stock:

1. Test closing prices.
2. Test daily returns.
3. Save results into a DataFrame.
4. Export results as `results/tables/adf_results.csv`.

### Observation Across Stocks

Most closing prices had:

* p-value greater than 0.05.
* Non-stationary.

Most daily returns had:

* p-value less than 0.05.
* Stationary.

---

# 11. Rolling Mean and Rolling Standard Deviation

Rolling statistics help visualize stationarity.

### Rolling Mean

Average over a moving window.

Example window:

30 trading days.

Purpose:

Check whether the mean stays stable.

### Rolling Standard Deviation

Standard deviation over a moving window.

Purpose:

Check whether volatility stays relatively constant.

### Interpretation

If rolling mean and rolling standard deviation remain fairly stable, the series is more likely to be stationary.

---

# 12. Correlation vs Stationarity

These concepts are different.

| Correlation                                         | Stationarity                                                     |
| --------------------------------------------------- | ---------------------------------------------------------------- |
| Measures how two variables move together.           | Measures whether one series has constant statistical properties. |
| High correlation does **not** imply mean reversion. | Stationarity is required for many mean-reversion methods.        |

### Important Project Insight

Correlation is **not** enough for pairs trading.

Week 3 introduces **cointegration**, which is stronger than correlation.

---

# 13. Python Functions Learned

## Pandas

| Function          | Purpose                       |
| ----------------- | ----------------------------- |
| `pct_change()`    | Calculate daily returns.      |
| `dropna()`        | Remove missing values.        |
| `rolling(window)` | Calculate rolling statistics. |
| `mean()`          | Rolling average.              |
| `std()`           | Rolling standard deviation.   |
| `DataFrame()`     | Store ADF results.            |
| `to_csv()`        | Save results.                 |

## Statsmodels

| Function     | Purpose               |
| ------------ | --------------------- |
| `adfuller()` | Perform the ADF test. |

---

# 14. Files Created During Week 2

## New Python Files

* `src/stationarity.py`
* `scripts/stationarity_analysis.py`

## Output Files

### Figures

* `stationarity_price_vs_return.png`
* `rolling_statistics.png`

### Tables

* `adf_results.csv`

---

# 15. Key Takeaways

* Stationarity is the mathematical foundation of statistical arbitrage.
* Stock prices generally behave like random walks and are non-stationary.
* Returns are often stationary because they remove the trend in prices.
* The ADF test is used to statistically verify stationarity.
* A p-value less than 0.05 indicates a stationary series.
* Correlation alone is insufficient for selecting trading pairs.

---

# Week 2 Checklist

* Learned stationarity and non-stationarity.
* Understood random walks and unit roots.
* Implemented the Augmented Dickey-Fuller test.
* Tested prices and returns for TCS.
* Tested ADF on multiple NIFTY stocks.
* Generated rolling statistics plots.
* Saved ADF results into a CSV for later analysis.

---

# Preparation for Week 3

Next week answers the question:

**Can two non-stationary stock prices combine to form one stationary spread?**

Topics to learn next:

* Correlation vs Cointegration.
* Engle-Granger Cointegration Test.
* Spread construction.
* Residual stationarity testing.
* Selecting statistically valid trading pairs.
