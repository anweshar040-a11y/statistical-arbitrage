# Week 5 — Backtesting Engine & Performance Metrics

> Project: Statistical Arbitrage — Cointegration-Based Pairs Trading with OLS Hedge Ratio

---

# Week 5 Goals

In Week 5, we convert our trading strategy into a **historical trading simulator**.

Until Week 4, the project only generated buy/sell signals from the spread's Z-score.

Week 5 answers the important question:

**"If we actually traded these signals using ₹100,000, how much money would we make or lose?"**

---

## Week 5 Deliverables

- Backtesting engine.
- Trade log.
- Daily strategy returns.
- Portfolio value (Equity Curve).
- Daily Profit & Loss.
- Drawdown calculation.
- Performance summary CSV.
- Equity curve and performance plots.

---

# Week 5 Project Flow

```text
Historical Prices
        │
        ▼
Spread Calculation
        │
        ▼
Z-Score
        │
        ▼
Trading Signals
        │
        ▼
Positions (Hold Long / Short)
        │
        ▼
Backtester
        │
        ▼
Portfolio Value
        │
        ▼
Performance Metrics
```

---

# Files Added During Week 5

```text
src/
├── backtester.py
├── performance.py

scripts/
├── run_backtest.py

results/
├── tables/
│   ├── trade_results.csv
│   ├── equity_curve.csv
│   └── performance_summary.csv
│
└── figures/
    ├── equity_curve.png
    ├── cumulative_returns.png
    ├── daily_pnl.png
    └── drawdown_curve.png
```

---

# DataFrame Evolution

Week 5 adds several new columns to the existing `prices` DataFrame.

| Week | New Columns |
|------|-------------|
| Week 1 | TCS, INFY |
| Week 3 | Spread |
| Week 4 | Z-Score, Signal, Position |
| Week 5 | Spread Change, Transaction Cost, Strategy Return, Portfolio Value, Daily PnL, Cumulative Return, Running Peak, Drawdown |

Final DataFrame:

| Date | Spread | Signal | Position | Spread Change | Strategy Return | Portfolio Value | Drawdown |
|------|--------|--------|----------|--------------|----------------|----------------|----------|

---

# Part 1 — Backtesting

## What is Backtesting?

Backtesting is the process of testing a trading strategy on historical data.

Instead of risking real money, we simulate trades using past prices.

Purpose:

- Check whether the strategy would have been profitable.
- Measure risk.
- Compare different trading strategies.

---

# Backtesting Logic

Every trading day:

1. Check today's position.
2. Calculate today's spread movement.
3. Convert spread movement into portfolio return.
4. Update portfolio value.

---

## Formula — Spread Change

Spread measures the price difference between two stocks.

Daily spread movement is:

```math
Spread Change_t = Spread_t - Spread_{t-1}
```

Example:

| Date | Spread | Spread Change |
|------|--------|---------------|
| Jan 1 | 191 | 0 |
| Jan 2 | 181 | -10 |
| Jan 3 | 170 | -11 |
| Jan 4 | 173 | +3 |

Interpretation:

- Positive Spread Change → Spread increased.
- Negative Spread Change → Spread decreased.

---

## Formula — Position

Position represents whether a trade is currently open.

| Position | Meaning |
|----------|---------|
| 1 | Long Spread |
| -1 | Short Spread |
| 0 | No Trade |

Important difference:

| Signal | Position |
|--------|----------|
| Entry instruction | Current holding |

Position stays open until exit condition.

Example:

| Date | Signal | Position |
|------|--------|----------|
| Jan 1 | 1 | 1 |
| Jan 2 | 0 | 1 |
| Jan 3 | 0 | 1 |
| Jan 4 | 0 | 0 |

---

## Why use Position.shift(1)?

Today's trade can only earn money starting tomorrow.

Using today's signal to calculate today's return would create **look-ahead bias**.

```python
Position.shift(1)
```

Example:

| Date | Position | Shifted Position |
|------|----------|------------------|
| Monday | 1 | 0 |
| Tuesday | 1 | 1 |
| Wednesday | 1 | 1 |

The strategy enters after Monday closes.

Returns begin Tuesday.

---

## Formula — Strategy Return

Portfolio return comes from spread movement.

```math
Strategy Return =
Position_{t-1}
\times
\frac{Spread Change_t}{Capital}
```

Where:

- Position = Long / Short / Flat.
- Spread Change = Today's spread movement.
- Capital = ₹100,000.

Example:

Spread increases by ₹20.

Long position:

```math
20/100000 = 0.0002 = 0.02\%
```

Short position:

```math
(-20)/100000 = -0.0002
```

---

# Transaction Cost

Backtests should include trading costs.

Assumptions:

| Cost | Value |
|------|------|
| Brokerage + Taxes | 0.10% |
| Slippage | 0.05% |
| Total | 0.15% |

Transaction cost is charged only when a position changes.

```math
Transaction Cost =
Trade Change
\times
(Transaction Cost + Slippage)
```

---

# Slippage

Slippage is the difference between expected execution price and actual execution price.

Example:

Expected Buy = ₹1500

Actual Buy = ₹1501.50

Extra ₹1.50 paid because of market movement.

Backtests subtract slippage to become more realistic.

---

# Trade Log

Each completed trade becomes one row.

Trade Log contains:

| Column | Meaning |
|--------|---------|
| Entry Date | Trade opened |
| Exit Date | Trade closed |
| Direction | Long / Short |
| Entry Spread | Spread at entry |
| Exit Spread | Spread at exit |
| Return | Percentage return |

---

## Trade Return Formula

### Long Trade

```math
Return =
\frac{Exit Spread - Entry Spread}
{|Entry Spread|}
```

### Short Trade

```math
Return =
\frac{Entry Spread - Exit Spread}
{|Entry Spread|}
```

Reason:

Short trades profit when spread decreases.

---

# Part 2 — Portfolio Simulation

## Initial Capital

Portfolio starts with:

```math
100000
```

Every daily return changes portfolio value.

---

## Formula — Portfolio Value

```math
Portfolio_t =
Portfolio_{t-1}
\times
(1 + Strategy Return_t)
```

Example:

| Day | Strategy Return | Portfolio |
|----|-----------------|-----------|
| Start | — | 100000 |
| Day 1 | +0.001 | 100100 |
| Day 2 | -0.002 | 99899 |

Portfolio compounds over time.

---

## Equity Curve

The equity curve plots portfolio value through time.

Purpose:

- Visualize growth.
- Identify profitable periods.
- Identify losing periods.

Output:

`results/figures/equity_curve.png`

---

# Daily Profit & Loss

Daily P&L measures money earned or lost each day.

Formula:

```math
DailyPnL =
Portfolio_t
-
Portfolio_{t-1}
```

Example:

| Day | Portfolio | Daily PnL |
|----|-----------|-----------|
| Day 1 | 100000 | 0 |
| Day 2 | 100150 | +150 |
| Day 3 | 99920 | -230 |

Output:

`daily_pnl.png`

---

# Cumulative Return

Cumulative return measures total portfolio growth from the start.

Formula:

```math
Cumulative Return =
\frac{Portfolio_t}{Initial Capital}
-
1
```

Example:

Portfolio = ₹108000

```math
108000/100000 -1 = 8\%
```

Output:

`cumulative_returns.png`

---

# Running Peak

Running Peak stores the highest portfolio value seen so far.

Formula:

```math
Running Peak =
cummax(Portfolio Value)
```

Example:

| Portfolio | Running Peak |
|-----------|--------------|
| 100000 | 100000 |
| 104000 | 104000 |
| 102000 | 104000 |
| 105500 | 105500 |

Peak never decreases.

---

# Drawdown

Drawdown measures how far the portfolio has fallen from its highest point.

Formula:

```math
Drawdown =
\frac{Portfolio - Peak}{Peak}
```

Example:

Peak = ₹104000

Portfolio = ₹102000

```math
(102000-104000)/104000 = -1.92\%
```

Interpretation:

Portfolio is 1.92% below its highest historical value.

Output:

`drawdown_curve.png`

---

# Maximum Drawdown

Maximum Drawdown is the largest drawdown during the entire backtest.

Formula:

```math
Maximum Drawdown =
min(Drawdown)
```

Example:

Drawdowns:

0%

-2%

-5%

-12%

-7%

Maximum Drawdown = **-12%**

Why important?

It measures worst historical loss.

---

# Part 3 — Performance Metrics

Performance metrics summarize the trading strategy.

Generated in:

`src/performance.py`

Saved as:

`performance_summary.csv`

---

## Performance Summary Table

| Metric | Meaning |
|--------|---------|
| Initial Capital | Starting portfolio value |
| Final Portfolio Value | Ending portfolio value |
| Total Return (%) | Overall portfolio gain/loss |
| Total Trades | Number of completed trades |
| Winning Trades | Trades with positive return |
| Losing Trades | Trades with negative return |
| Win Rate (%) | Percentage of winning trades |
| Average Trade Return (%) | Mean trade return |
| Maximum Drawdown (%) | Largest portfolio decline |

---

## Initial Capital

Formula:

```math
Initial Capital = Portfolio_0
```

Uses first portfolio value.

---

## Final Portfolio Value

Formula:

```math
Final Capital = Portfolio_T
```

Uses last portfolio value.

---

## Total Return

Formula:

```math
Total Return =
\left(
\frac{Final}{Initial}
-
1
\right)
\times100
```

Example:

Initial = ₹100000

Final = ₹83657

```math
-16.34\%
```

Interpretation:

Portfolio lost 16.34%.

---

## Total Trades

Formula:

```math
Total Trades =
Number\ of\ Completed\ Trades
```

Each row in Trade Log equals one completed trade.

---

## Winning Trades

Winning trade:

```math
Trade Return > 0
```

Count all winning trades.

---

## Losing Trades

Losing trade:

```math
Trade Return \le 0
```

Count all losing trades.

---

## Win Rate

Formula:

```math
Win Rate =
\frac{Winning Trades}{Total Trades}
\times100
```

Example:

Winning Trades = 41

Total Trades = 60

```math
68.33\%
```

Important:

High win rate does **not** guarantee profitability.

---

## Average Trade Return

Formula:

```math
Average Trade Return =
Mean(Trade Returns)
```

Example:

Returns:

2%

1%

-3%

Average = 0%.

This measures average performance per completed trade.

---

## Maximum Drawdown

Formula:

```math
Maximum Drawdown =
Minimum(Drawdown)
```

Example:

Drawdowns:

0%

-4%

-8%

-12%

Maximum Drawdown = -12%.

---

# Performance Metrics Example

| Metric | Example Value |
|--------|---------------|
| Initial Capital | ₹100000 |
| Final Portfolio Value | ₹83657.50 |
| Total Return | -16.34% |
| Total Trades | 60 |
| Winning Trades | 41 |
| Losing Trades | 19 |
| Win Rate | 68.33% |
| Average Trade Return | 0.95% |
| Maximum Drawdown | -16.34% |

---

# Understanding the Results

A strategy can have:

- High Win Rate.
- Negative Total Return.

Reason:

Winning trades are smaller than losing trades.

Example:

| Wins | Losses |
|------|--------|
| +1% | -6% |
| +2% | -5% |
| +1% | -8% |

More winning trades, but overall loss.

This is why performance metrics must be analyzed together.

---

# Week 5 Figures Generated

| Figure | Purpose |
|--------|---------|
| `equity_curve.png` | Portfolio value through time. |
| `daily_pnl.png` | Daily money earned/lost. |
| `cumulative_returns.png` | Total percentage return over time. |
| `drawdown_curve.png` | Portfolio decline from previous peak. |

---

# Week 5 Key Quant Concepts

| Concept | Summary |
|--------|---------|
| Backtesting | Simulate trades on historical data. |
| Position | Current trade being held. |
| Strategy Return | Daily portfolio return from spread movement. |
| Transaction Cost | Brokerage and taxes deducted on trades. |
| Slippage | Execution price differs from expected price. |
| Equity Curve | Portfolio value over time. |
| Daily P&L | Daily profit or loss in rupees. |
| Cumulative Return | Total portfolio growth since start. |
| Running Peak | Highest portfolio value reached so far. |
| Drawdown | Decline from running peak. |
| Maximum Drawdown | Largest historical portfolio decline. |
| Win Rate | Percentage of profitable trades. |
| Average Trade Return | Average return per completed trade. |

---

# Week 5 Formula Cheat Sheet

```math
Spread = INFY - \beta \times TCS
```

```math
Spread Change = Spread_t - Spread_{t-1}
```

```math
Strategy Return =
Position_{t-1}
\times
\frac{Spread Change}{Capital}
```

```math
Portfolio_t =
Portfolio_{t-1}
(1 + Strategy Return_t)
```

```math
DailyPnL =
Portfolio_t - Portfolio_{t-1}
```

```math
Cumulative Return =
\frac{Portfolio_t}{Portfolio_0}-1
```

```math
Drawdown =
\frac{Portfolio - Peak}{Peak}
```

```math
Win Rate =
\frac{Winning Trades}{Total Trades}\times100
```

```math
Total Return =
\left(
\frac{Final Capital}{Initial Capital}
-
1
\right)\times100
```

```math
Maximum Drawdown =
Minimum(Drawdown)
```

---

# Week 5 Interview Questions

### Technical

1. What is backtesting?
2. Why do we shift positions by one day?
3. Why is spread difference used instead of percentage change?
4. What is look-ahead bias?
5. Why include transaction costs and slippage?

### Quant Finance

6. Explain equity curve.
7. Explain drawdown.
8. Difference between drawdown and daily loss.
9. Why can a strategy have a high win rate but negative return?
10. What does maximum drawdown tell an investor?

---

# Week 5 Completion Checklist

- [x] Build backtesting engine.
- [x] Generate trade log.
- [x] Calculate strategy returns.
- [x] Simulate portfolio value.
- [x] Add transaction costs and slippage.
- [x] Calculate Daily P&L.
- [x] Calculate cumulative returns.
- [x] Calculate running peak and drawdown.
- [x] Generate performance summary CSV.
- [x] Save equity curve, drawdown, cumulative return, and daily P&L plots.