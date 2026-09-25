# Week 4 Notes — Mean Reversion Trading Strategy

## Project Context

**Project:** Statistical Arbitrage — Cointegration-Based Pairs Trading with a Kalman Filter Hedge Ratio

### Goal of Week 4

Convert the stationary spread from Week 3 into a complete **trading strategy** by generating entry, exit, and position signals.

---

# 1. Mean Reversion

Mean reversion is the idea that a variable temporarily moves away from its long-term average but eventually returns toward it.

In pairs trading, we assume the **spread** between two cointegrated stocks is mean-reverting.

### Mean Reversion Equation

Spreadₜ = μ + εₜ

Where:

* μ = Long-term average spread.
* εₜ = Temporary deviation from the average.

### Trading Intuition

* Spread becomes unusually high → Expect it to fall back.
* Spread becomes unusually low → Expect it to rise back.

The strategy trades these temporary deviations.

---

# 2. Spread Review

From Week 3:

Spread = Y − βX

Where:

* Y = Price of one stock.
* X = Price of the second stock.
* β = Hedge ratio estimated using Ordinary Least Squares (OLS).

The spread is the series used for trading, not the individual stock prices.

---

# 3. Z-Score

A z-score measures how far the spread is from its average in terms of standard deviations.

### Formula

Z = (Spread − μ) / σ

Where:

* μ = Mean spread.
* σ = Standard deviation of spread.

### Interpretation

| Z-Score        | Interpretation                 |
| -------------- | ------------------------------ |
| 0              | Spread is at its mean.         |
| Positive       | Spread is above its average.   |
| Negative       | Spread is below its average.   |
| Large positive | Spread is unusually expensive. |
| Large negative | Spread is unusually cheap.     |

The z-score standardizes spreads so different pairs can be compared using the same thresholds.

---

# 4. Rolling Z-Score

Instead of using one mean and one standard deviation for the entire dataset, calculate them over a moving window.

### Rolling Mean

Average spread over the previous 30 trading days.

### Rolling Standard Deviation

Volatility of the spread over the previous 30 trading days.

### Rolling Z-Score Formula

Zₜ = (Spreadₜ − Rolling Meanₜ) / Rolling Stdₜ

### Why Rolling Statistics?

Markets change over time.

Rolling statistics allow the strategy to adapt to changing market conditions instead of assuming one constant average.

---

# 5. Trading Signals

The trading strategy uses z-score thresholds.

| Condition | Action            |       |                 |
| --------- | ----------------- | ----- | --------------- |
| Z > +2    | Short the spread. |       |                 |
| Z < −2    | Long the spread.  |       |                 |
|           | Z                 | < 0.5 | Exit the trade. |

### Long Spread

Buy the undervalued side of the pair and sell the overvalued side.

### Short Spread

Sell the overvalued side of the pair and buy the undervalued side.

### Exit Signal

Close both positions when the spread returns close to its long-term average.

---

# 6. Long Spread vs Short Spread

Assume the trading pair is **TCS–Infosys**.

### Long Spread

Condition:

Z-score < −2

Trade:

* Buy TCS.
* Sell Infosys.

Expectation:

The spread will increase toward its mean.

### Short Spread

Condition:

Z-score > +2

Trade:

* Sell TCS.
* Buy Infosys.

Expectation:

The spread will decrease toward its mean.

---

# 7. Signal DataFrame

A signal table stores trading decisions for every trading day.

### Columns

| Column   | Meaning                      |
| -------- | ---------------------------- |
| Date     | Trading day.                 |
| Z-Score  | Current standardized spread. |
| Signal   | Trading instruction.         |
| Position | Current active position.     |

### Signal Values

| Value | Meaning          |
| ----- | ---------------- |
| 1     | Long spread.     |
| -1    | Short spread.    |
| 0     | No trade / Exit. |

---

# 8. Position Management

A signal indicates **when to enter**.

A position indicates **whether a trade is currently active**.

### Why Positions Are Needed

If z-score stays above +2 for several days:

* Enter one trade.
* Do not repeatedly enter new trades every day.

### Position States

| Position | Meaning                 |
| -------- | ----------------------- |
| 0        | No active trade.        |
| 1        | Holding a long spread.  |
| -1       | Holding a short spread. |

This logic is implemented using a position state machine.

---

# 9. State Machine Logic

The strategy moves between three states.

### Initial State

No position.

### Entry

* Signal = 1 → Enter long spread.
* Signal = -1 → Enter short spread.

### Exit

Return to position 0 when the exit condition is satisfied.

Purpose:

Prevent duplicate entries and keep only one active trade at a time.

---

# 10. Trade Log

A trade log records every completed trade.

### Information Stored

| Column     | Meaning               |
| ---------- | --------------------- |
| Entry Date | Date trade opened.    |
| Exit Date  | Date trade closed.    |
| Direction  | Long or Short spread. |
| Entry Z    | Z-score at entry.     |
| Exit Z     | Z-score at exit.      |

The trade log becomes the input for backtesting in Week 5.

---

# 11. Signal Visualization

Two important plots were created.

## Spread Signal Plot

Shows:

* Spread line.
* Buy markers.
* Sell markers.

Purpose:

Visual verification of trading entries.

## Z-Score Signal Plot

Shows:

* Rolling z-score.
* Buy markers.
* Sell markers.
* Threshold lines (+2, -2, 0).

Purpose:

Verify that signals occur when z-score crosses thresholds.

---

# 12. Stop-Loss Rule

Mean reversion is not guaranteed immediately.

### Stop-Loss

Example rule:

Exit if:

* Z-score exceeds +3.
* Z-score goes below -3.

Purpose:

Limit losses if the spread continues moving away from equilibrium.

---

# 13. Holding Period

A trade should not remain open forever.

### Maximum Holding Period

Example:

20 trading days.

Purpose:

* Reduce capital being locked.
* Protect against regime changes.

---

# 14. Strategy Pipeline

Complete Week 4 workflow.

1. Load two cointegrated stocks.
2. Calculate hedge ratio.
3. Construct spread.
4. Calculate rolling z-score.
5. Generate trading signals.
6. Generate positions.
7. Record trades.
8. Save signal and trade logs.
9. Visualize signals.

This is the first complete trading strategy in the project.

---

# 15. Python Concepts Learned

## Pandas

| Function     | Purpose                                  |
| ------------ | ---------------------------------------- |
| `rolling()`  | Moving window calculations.              |
| `mean()`     | Rolling average.                         |
| `std()`      | Rolling volatility.                      |
| `loc[]`      | Create trading signals using conditions. |
| `iterrows()` | Iterate through daily signals.           |
| `to_csv()`   | Save signal and trade logs.              |

## Matplotlib

| Function    | Purpose                  |
| ----------- | ------------------------ |
| `plot()`    | Plot spread and z-score. |
| `scatter()` | Plot buy/sell markers.   |
| `axhline()` | Draw threshold lines.    |
| `savefig()` | Save strategy figures.   |

---

# 16. Files Created During Week 4

## Source Files

* `src/statistics_utils.py`
* `src/strategy.py`

## Scripts

* `scripts/spread_analysis.py`
* `scripts/strategy_analysis.py`

## Tables

* `signal_log.csv`
* `trade_log.csv`
* `strategy_summary.csv`

## Figures

* `tcs_infy_spread.png`
* `rolling_zscore.png`
* `spread_signals.png`
* `zscore_signals.png`

---

# 17. Key Takeaways

* Mean reversion is the trading assumption behind statistical arbitrage.
* The spread is converted into a standardized z-score using rolling statistics.
* Entry signals occur when z-score moves beyond predefined thresholds.
* Exit signals occur when z-score returns close to equilibrium.
* Positions prevent repeated entries while a trade is active.
* Every completed trade is recorded in a trade log for future backtesting.

---

# Week 4 Checklist

* Understood mean reversion.
* Learned rolling z-score.
* Generated entry and exit signals.
* Implemented long and short spread logic.
* Built position management.
* Created trade log.
* Visualized spread and z-score signals.
* Added basic stop-loss and holding period rules.

---

# Preparation for Week 5

Week 5 focuses on **Backtesting**.

Topics to learn next:

* Trade execution simulation.
* Daily profit and loss (P&L).
* Portfolio value over time.
* Transaction costs.
* Equity curve generation.
* Win rate and cumulative returns.
