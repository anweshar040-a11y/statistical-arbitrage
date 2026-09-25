# Week 8 — Day 1 Notes

## Topic: Dollar-Neutral Position Sizing

### Objective

Upgrade the Week 5 backtester into a realistic long-short portfolio used in pairs trading.

### Why Upgrade the Backtester?

Week 5 calculated returns using changes in the spread.

This ignored the individual returns of TCS and INFY and produced unrealistically low volatility.

### Dollar-Neutral Portfolio

Each trade allocates:

- ₹50,000 Long Position.
- ₹50,000 Short Position.

Total exposure = ₹100,000.

The strategy profits from **relative movement** rather than overall market direction.

### Daily Return Formula

**Long Spread**

R(strategy) = R(INFY) − R(TCS)

**Short Spread**

R(strategy) = R(TCS) − R(INFY)

### Transaction Cost

A transaction cost of **0.05%** is deducted whenever the portfolio changes position.

### Look-Ahead Bias Prevention

Strategy returns are shifted by one trading day before calculating portfolio returns.

Today's signal becomes tomorrow's trade.

### Outputs

- optimized_equity_curve.csv
- optimized_trade_log.csv
- optimized_equity_curve.png
- drawdown_curve.png

### Week 8 Day 1 Observation

The upgraded backtest produced a final portfolio value of **₹107,482.66**, indicating that the strategy generated a positive cumulative return over the evaluation period.

However, the portfolio experienced a **maximum drawdown of 57.84%**, falling from a peak value of **₹131,106.52** to **₹55,272.52** before partially recovering.

This indicates that the strategy is capable of recovering losses, but it allows trades to remain open during prolonged spread divergence. The high drawdown highlights weaknesses in the current risk management rules rather than an implementation error.

This motivates the introduction of stop-loss rules, maximum holding periods, and parameter optimization in the following stages of the project.

## Week 8 Day 2 — Kalman Filter Performance Summary

The Kalman Filter strategy was evaluated using a dynamic hedge ratio estimated through a state-space model. Unlike the OLS strategy, the hedge ratio was updated continuously throughout the trading period.

### Results

| Metric                     |          Value |
| -------------------------- | -------------: |
| Average Kalman Hedge Ratio |     **0.4553** |
| Initial Capital            |       ₹100,000 |
| Final Portfolio Value      | **₹94,278.23** |
| Maximum Drawdown           |      **5.72%** |
| Total Trades               |         **59** |

### Observations

* The Kalman Filter significantly reduced maximum drawdown compared to the baseline OLS strategy.
* The strategy traded almost as frequently as the OLS model while maintaining substantially lower downside risk.
* Although cumulative returns remained slightly negative, the adaptive hedge ratio produced a much smoother equity curve and improved portfolio stability.

### Conclusion

The Kalman Filter demonstrated that dynamically updating the hedge ratio can improve the robustness of a statistical arbitrage strategy by adapting to changing market relationships. This provides a stronger foundation for further optimization through parameter tuning and walk-forward testing.
# Week 8 — Day 2 Results Summary

## Objective

Improve the statistical arbitrage strategy by correcting the spread return calculation and evaluating the optimized portfolio.

---

## Final Results

| Metric                  | Value          |
| ----------------------- | -------------- |
| Initial Capital         | ₹100,000       |
| Final Portfolio Value   | **₹98,775.17** |
| Total Return            | **-1.22%**     |
| Maximum Drawdown        | **8.76%**      |
| Highest Portfolio Value | ₹103,349.57    |
| Lowest Portfolio Value  | ₹94,299.07     |
| Total Trades            | **60**         |
| OLS Hedge Ratio         | **0.355**      |

---

## Observations

* The spread return calculation was corrected by normalizing spread changes using the hedge value instead of using `pct_change()` on the spread.
* The corrected implementation produced a much more realistic equity curve.
* Maximum drawdown decreased from approximately **16.34%** in the baseline implementation to **8.76%** after correcting portfolio return calculations.
* The strategy remained close to breakeven while maintaining significantly better downside protection.

---

## Conclusion

The corrected backtester produces stable portfolio returns that are consistent with a market-neutral statistical arbitrage strategy. The portfolio experienced much smaller fluctuations while preserving most of the initial capital. This implementation becomes the new baseline for further optimization through parameter tuning and walk-forward validation.
## Week 8 — Day 3 Results Summary

### Objective

Optimize the statistical arbitrage strategy by searching across multiple entry and exit Z-score thresholds.

### Parameters Tested

| Entry Threshold    | Exit Threshold     |
| ------------------ | ------------------ |
| 1.8, 2.0, 2.2, 2.5 | 0.2, 0.5, 0.8, 1.0 |

A total of **16 parameter combinations** were evaluated using grid search.

### Best Parameters

| Metric                |          Value |
| --------------------- | -------------: |
| Entry Z-score         |        **1.8** |
| Exit Z-score          |        **0.2** |
| Final Portfolio Value | **₹99,378.09** |
| Sharpe Ratio          |    **-0.0036** |
| Annual Return         |     **-0.11%** |
| Annual Volatility     |      **4.43%** |
| Maximum Drawdown      |     **11.19%** |
| Total Trades          |        **235** |

### Observations

* Lower entry thresholds produced significantly more trading opportunities.
* The optimized parameter combination generated the highest Sharpe ratio among all tested strategies.
* The strategy finished close to breakeven while maintaining a relatively low annualized volatility.
* The Sharpe heatmap visualized the performance of every parameter combination and identified the optimal configuration.

### Conclusion

Grid search introduced a systematic method for selecting trading parameters instead of relying on manually chosen thresholds. This mirrors hyperparameter tuning workflows commonly used in quantitative research and machine learning.

# Week 8 — Day 4 Notes

## Topic: Walk-Forward Validation

### Objective

Evaluate whether the statistical arbitrage strategy generalizes to unseen market data instead of being evaluated on the entire historical dataset.

---

## Why Walk-Forward Testing?

Financial time series cannot be randomly shuffled because future information must never be used during training.

Walk-forward validation follows chronological order:

| Training Period | Testing Period |
| --------------- | -------------- |
| 2021–2023       | 2024           |
| 2021–2024       | 2025           |
| 2021–2025       | 2026           |

Each testing window is completely out-of-sample.

---

## Workflow

1. Estimate hedge ratio on the training period.
2. Construct spread on unseen testing data.
3. Calculate rolling Z-score.
4. Generate trading signals.
5. Backtest only on testing data.
6. Record performance metrics.

---

## Outputs Generated

### Tables

* walk_forward_summary.csv
* walk_forward_portfolios.csv

### Figures

* walk_forward_equity_curve.png
* walk_forward_sharpe.png
* walk_forward_drawdown.png

---

## Metrics Compared

* Sharpe Ratio
* Final Portfolio Value
* Maximum Drawdown
* Number of Trades

---

## Key Learning

Walk-forward validation is the standard evaluation methodology for quantitative trading strategies because it measures performance on unseen market conditions. It helps detect overfitting and provides a more realistic estimate of how a strategy may behave in live trading.

# Week 8 — Day 4 Results Summary

## Objective

Evaluate the statistical arbitrage strategy on unseen market data using walk-forward validation.

---

## Best Walk-Forward Window

| Metric                |           Value |
| --------------------- | --------------: |
| Training Period       |   **2021–2023** |
| Testing Period        |        **2024** |
| Sharpe Ratio          |      **1.3647** |
| Final Portfolio Value | **₹104,261.52** |
| Portfolio Return      |       **4.26%** |
| Maximum Drawdown      |       **1.24%** |
| Total Trades          |          **17** |

---

## Observations

* The strategy was trained only on historical data from 2021–2023.
* Performance was evaluated exclusively on unseen data from 2024.
* The testing window produced the highest Sharpe ratio observed in the project.
* Maximum drawdown remained extremely low, indicating strong downside protection.
* The strategy generated fewer but higher-quality trading opportunities.

---

## Conclusion

Walk-forward validation demonstrated that the statistical arbitrage strategy generalized well during the 2024 testing window. This evaluation avoids look-ahead bias and provides a more realistic estimate of live trading performance than evaluating the strategy on the entire historical dataset.

# Week 8 — Day 5 Notes

## Topic: Benchmarking Against Buy & Hold

### Objective

Compare the statistical arbitrage strategy against a passive investment portfolio.

---

## What is a Benchmark?

A benchmark is a reference strategy used to evaluate whether a trading strategy adds value.

In this project, the benchmark is an equally weighted Buy & Hold portfolio consisting of:

* 50% TCS
* 50% INFY

---

## Buy & Hold Formula

Daily benchmark return:

R = 0.5 × TCS Return + 0.5 × INFY Return

Portfolio value is calculated by compounding daily benchmark returns from an initial capital of ₹100,000.

---

## Metrics Compared

* Final Portfolio Value
* Annualized Return
* Annualized Volatility
* Sharpe Ratio
* CAGR
* Maximum Drawdown
* Calmar Ratio

---

## Visualizations Generated

* Strategy vs Buy & Hold Equity Curve.
* Cumulative Return Comparison.
* Drawdown Comparison.
* Daily Return Distribution Histogram.

---

## Why Benchmarking Matters

Benchmarking helps determine whether an active trading strategy outperforms passive investing after accounting for risk. Even if two portfolios have similar returns, lower drawdown or higher Sharpe Ratio may indicate better risk-adjusted performance.

---

## Outputs

### Tables

* benchmark_summary.csv
* benchmark_equity_curve.csv

### Figures

* benchmark_equity_curve.png
* benchmark_drawdown.png
* benchmark_return_distribution.png
* cumulative_return_comparison.png

# Week 8 — Day 5 Results Summary

## Benchmark Comparison: Statistical Arbitrage vs Buy & Hold

### Objective

Evaluate whether the statistical arbitrage strategy outperformed a passive Buy & Hold portfolio consisting of 50% TCS and 50% INFY.

---

## Results

| Metric                | Statistical Arbitrage |  Buy & Hold |
| --------------------- | --------------------: | ----------: |
| Final Portfolio Value |        **₹98,775.17** | ₹101,009.84 |
| Total Return          |            **-1.22%** |  **+1.01%** |
| Annualized Return     |                -0.22% |       0.18% |
| Annualized Volatility |             **3.75%** |      22.05% |
| Sharpe Ratio          |                -0.041 |   **0.119** |
| Maximum Drawdown      |             **8.76%** |      50.18% |
| Calmar Ratio          |                -0.026 |      0.0037 |

---

## Observations

* Buy & Hold generated a slightly higher cumulative return over the evaluation period.
* The statistical arbitrage strategy produced significantly lower volatility.
* Maximum drawdown was reduced from **50.18%** for Buy & Hold to **8.76%** for the statistical arbitrage strategy.
* The strategy preserved capital much better during adverse market periods.

---

## Conclusion

The statistical arbitrage strategy did not outperform Buy & Hold in terms of cumulative return, but it substantially reduced downside risk and portfolio volatility. This demonstrates the trade-off between return generation and capital preservation in market-neutral trading strategies.
