# Week 3 — Cointegration, Hedging & Engle–Granger (Theory Notes)

**Quant Roadmap Project:** Statistical Arbitrage — Cointegration-Based Pairs Trading

**Goal of Week 3:** Learn the finance theory behind pairs trading before writing the code.

---

# Week 3 Learning Objectives

By the end of Week 3, I should understand:

* Hedging
* Hedge Ratio (β)
* Spread
* Residual
* Correlation vs Cointegration
* OLS Regression
* Engle–Granger Cointegration Test
* ADF Test in Cointegration
* Z-Score Trading Signals

---

# 1. Hedging

## Definition

Hedging is a **risk management strategy** used to reduce the risk of one investment by taking another related position.

Instead of betting that the overall market will go up or down, pairs trading bets on the **relative movement** between two stocks.

## Intuition

Suppose I believe **TCS** is undervalued.

### Without Hedging

* Buy TCS.
* Profit depends on:

  * TCS performance.
  * IT sector performance.
  * Overall market movement.

If the entire market falls, TCS may fall even if it is fundamentally undervalued.

### With Hedging

* Buy TCS.
* Short Infosys.

Now I am betting that **TCS performs better than Infosys**, not that the IT sector rises.

## Why Hedging is Important in Pairs Trading

Pairs trading is a **market-neutral strategy**.

* Long one stock.
* Short another related stock.

Market-wide movements affect both stocks similarly, so the trade focuses on their price difference rather than market direction.

**Key Point:** Hedging removes most market and sector risk and leaves mainly the relative pricing relationship.

---

# 2. Hedge Ratio (β)

## Definition

The **hedge ratio** tells us how many units of one stock are needed to hedge one unit of another stock.

It balances the long and short positions.

## Formula

Spread = Price_A − β × Price_B

Where:

* Price_A = first stock.
* Price_B = second stock.
* β = hedge ratio.

## Example

| Stock   | Price |
| ------- | ----- |
| TCS     | ₹4200 |
| Infosys | ₹1600 |

If β = **2.5**

Trade becomes:

* Long 1 TCS.
* Short 2.5 Infosys.

This creates a balanced hedge.

## Interpretation of β

* β is **not** the stock market beta from CAPM.
* In pairs trading, β is simply a scaling factor estimated from historical prices.
* It represents the long-term relationship between two stocks.

## Why Do We Need β?

Stocks have different price levels.

Subtracting prices directly is meaningless.

β rescales one stock so both prices become comparable.

**Key Point:** Hedge ratio converts two stocks into comparable units.

---

# 3. Correlation vs Cointegration

## Correlation

### Definition

Correlation measures **how similarly two variables move**.

Range:

* +1 = move together perfectly.
* 0 = no linear relationship.
* -1 = move in opposite directions.

### What Correlation Measures

* Direction of movement.
* Strength of linear relationship.

### Limitation

Two stocks can have high correlation because both trend upward.

They may still drift apart forever.

**High correlation does NOT mean a good pairs trade.**

---

## Cointegration

### Definition

Two non-stationary price series are cointegrated if a linear combination of them is stationary.

### Mathematical Idea

Price_A and Price_B are non-stationary.

Spread = Price_A − β × Price_B

If the spread is stationary, the stocks are cointegrated.

### Intuition

Two people walking with a rope.

* Both wander.
* They temporarily separate.
* The rope pulls them back together.

That rope represents cointegration.

## Correlation vs Cointegration Table

| Correlation                                     | Cointegration                                |
| ----------------------------------------------- | -------------------------------------------- |
| Measures short-term movement similarity.        | Measures long-term equilibrium relationship. |
| Uses returns or movements.                      | Uses prices and spread.                      |
| Can stay high while prices drift apart forever. | Spread returns to its long-term mean.        |
| Used to screen candidate pairs.                 | Used to validate pairs for trading.          |

**Important:** Correlation is necessary for finding candidates but cointegration determines whether the pair is tradable.

---

# 4. Spread

## Definition

Spread measures the **relative distance** between two stocks after adjusting for the hedge ratio.

## Formula

Spread = Price_A − β × Price_B

## Example

| Value         | Amount |
| ------------- | ------ |
| TCS Price     | 4200   |
| Infosys Price | 1600   |
| β             | 2.5    |

Spread = 4200 − 2.5 × 1600 = 200

## Interpretation

* Small spread → Relationship is normal.
* Large positive spread → Stock A looks expensive relative to Stock B.
* Large negative spread → Stock A looks cheap relative to Stock B.

## Why Spread Matters

Pairs trading trades the **spread**, not the individual stock prices.

The spread should fluctuate around an equilibrium value.

---

# 5. Mean Reversion

## Definition

A mean-reverting series tends to return to its long-term average after moving away from it.

## Intuition

Rubber band analogy:

* Stretch the rubber band.
* Release it.
* It returns to its original shape.

Spread behaves similarly if the pair is cointegrated.

## Random Walk vs Mean Reversion

| Random Walk                    | Mean Reversion              |
| ------------------------------ | --------------------------- |
| Wanders indefinitely.          | Returns toward equilibrium. |
| Non-stationary.                | Stationary.                 |
| Shocks have permanent effects. | Shocks gradually disappear. |

**Pairs trading profits because spreads are assumed to mean revert.**

---

# 6. OLS Regression (Ordinary Least Squares)

## Purpose

OLS estimates the hedge ratio β.

## Regression Equation

Y = α + βX + ε

## Meaning of Each Symbol

| Symbol | Meaning                          |
| ------ | -------------------------------- |
| Y      | Price of Stock A.                |
| X      | Price of Stock B.                |
| α      | Intercept (baseline difference). |
| β      | Hedge ratio (slope).             |
| ε      | Residual (prediction error).     |

## What OLS Does

OLS fits the best straight line through historical prices.

It minimizes the squared prediction errors.

## Interpretation

Suppose:

Actual TCS = 4200

Predicted TCS = 4150

Residual = 4200 − 4150 = 50

Residual measures how far today's price is from its expected relationship.

---

# 7. Residual vs Spread

This is an important distinction.

## Residual

Residual is the error from regression.

Formula:

Residual = Actual Price − Predicted Price

Residual = Y − (α + βX)

## Spread

Spread is the tradable relationship between two assets.

Formula:

Spread = Price_A − β × Price_B

## Difference

| Spread                  | Residual                               |
| ----------------------- | -------------------------------------- |
| Uses hedge ratio only.  | Uses hedge ratio and intercept α.      |
| Trading interpretation. | Statistical regression interpretation. |

### In Practice

In most pairs trading implementations:

**Residuals are treated as the spread** after regression.

The residual time series is what we analyze and trade.

**Key Point:** Residual is the statistically estimated spread.

---

# 8. Engle–Granger Cointegration Test

## Purpose

Tests whether two non-stationary stocks have a stationary relationship.

## Why It Is Needed

High correlation is not enough.

Need to verify that the spread is stationary.

## Five-Step Procedure

### Step 1

Choose two stocks.

Example:

* TCS
* Infosys

### Step 2

Run OLS regression.

TCS = α + β × Infosys + ε

Estimate:

* α
* β

### Step 3

Extract residuals.

Residuals become the spread series.

### Step 4

Run the ADF test on residuals.

### Step 5

Interpret the result.

* Residual stationary → Cointegration exists.
* Residual non-stationary → No cointegration.

## Hypotheses

**Null Hypothesis (H₀):**

Residual has a unit root.

No cointegration.

**Alternative Hypothesis (H₁):**

Residual is stationary.

Cointegration exists.

## Interpretation

If ADF rejects the null hypothesis, the pair is cointegrated.

**Important:** ADF is run on residuals, not on returns, during the Engle–Granger test.

---

# 9. ADF Test in Cointegration

## Why Run ADF Again?

### Week 2

ADF tested stock prices.

Expected:

* Prices are non-stationary.

### Week 3

ADF tests residuals.

Expected:

* Residuals are stationary.

## Interpretation

| ADF Result     | Meaning                                  |
| -------------- | ---------------------------------------- |
| p-value < 0.05 | Residual stationary → Cointegrated pair. |
| p-value ≥ 0.05 | Residual non-stationary → Reject pair.   |

## Workflow

1. Prices are I(1).
2. Regression creates residuals.
3. Residuals should be I(0).
4. Stationary residuals imply cointegration.

---

# 10. Z-Score

## Why Do We Need It?

Raw spread values depend on stock prices.

Need a standardized measure.

## Formula

Z = (Spread − Mean Spread) / Standard Deviation of Spread

## Meaning of Each Term

| Term               | Meaning                     |
| ------------------ | --------------------------- |
| Spread             | Today's spread value.       |
| Mean Spread        | Historical average spread.  |
| Standard Deviation | Typical spread fluctuation. |

## Interpretation

| Z-Score | Meaning                 |
| ------- | ----------------------- |
| 0       | Spread at equilibrium.  |
| +1      | Slightly above average. |
| +2      | Unusually high spread.  |
| -2      | Unusually low spread.   |

## Trading Rules

| Condition        | Action        |
| ---------------- | ------------- |
| Z > +2           | Short spread. |
| Z < -2           | Long spread.  |
| Z returns near 0 | Exit trade.   |

## Why Z-Score Works

Z-score measures how many standard deviations the spread is away from its long-term mean.

Large deviations are expected to revert if the spread is stationary.

---

# 11. Market-Neutral Strategy

## Definition

A market-neutral strategy aims to remove exposure to the overall market.

## Pairs Trading Position

* Long undervalued stock.
* Short overvalued stock.

## Outcome

Profit depends on the convergence of the pair rather than market direction.

Even if the market falls, the strategy may still profit if the spread closes.

---

# Week 3 Summary (Important Exam Notes)

## Concepts to Remember

### Hedging

Reducing risk by taking an opposite or related position.

### Hedge Ratio (β)

Scaling factor that balances two stocks in a pair.

### Spread

Relative difference between two stocks after applying β.

### Residual

Regression prediction error; usually treated as the spread.

### Correlation

Measures similarity in movement but does not imply equilibrium.

### Cointegration

Two non-stationary price series have a stationary spread.

### Mean Reversion

Spread tends to return to its long-term average.

### OLS Regression

Estimates α and β and produces residuals.

### Engle–Granger Test

OLS Regression → Residuals → ADF Test on Residuals.

### Z-Score

Standardized spread used to generate entry and exit signals.

---

# Week 3 Flow (Very Important)

Prices (TCS & Infosys)

↓

OLS Regression

↓

Estimate Hedge Ratio (β)

↓

Compute Residual / Spread

↓

ADF Test on Residuals

↓

If Residual is Stationary

↓

Cointegrated Pair

↓

Calculate Z-Score

↓

Generate Long / Short Trading Signals

---

# Week 3 One-Line Cheat Sheet

* **Hedging:** Reduce market risk using a related position.
* **Hedge Ratio (β):** Number of shares of Stock B needed to hedge Stock A.
* **Spread:** Relative mispricing between two stocks.
* **Residual:** Regression error representing the spread after OLS.
* **Cointegration:** Stable long-term relationship between non-stationary prices.
* **Engle–Granger:** Regression followed by an ADF test on residuals.
* **Z-Score:** Measures how far the spread is from its historical average in standard deviation units.
