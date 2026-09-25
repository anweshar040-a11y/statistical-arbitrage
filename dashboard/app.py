import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------------

st.set_page_config(
    page_title="Statistical Arbitrage Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Statistical Arbitrage Trading Dashboard")
st.markdown("Cointegration-Based Pairs Trading with OLS and Kalman Filter")

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

strategy = pd.read_csv(
    "results/tables/equity_curve.csv",
    parse_dates=["Date"],
    index_col="Date"
)

trade_log = pd.read_csv(
    "results/tables/trade_results.csv"
)

kalman = pd.read_csv(
    "results/tables/kalman_backtest_summary.csv",
    parse_dates=["Date"],
    index_col="Date"
)

benchmark = pd.read_csv(
    "results/tables/benchmark_equity_curve.csv",
    parse_dates=["Date"],
    index_col="Date"
)

optimization = pd.read_csv(
    "results/tables/optimization_results.csv"
)

# -------------------------------------------------------
# CREATE MISSING COLUMNS
# -------------------------------------------------------

if "Drawdown" not in strategy.columns:
    strategy["Running Peak"] = strategy["Portfolio Value"].cummax()
    strategy["Drawdown"] = (
        strategy["Portfolio Value"] - strategy["Running Peak"]
    ) / strategy["Running Peak"]

if "Cumulative Return" not in strategy.columns:
    strategy["Cumulative Return"] = (
        strategy["Portfolio Value"] / 100000 - 1
    )

if "Drawdown" not in kalman.columns:
    kalman["Running Peak"] = kalman["Portfolio Value"].cummax()
    kalman["Drawdown"] = (
        kalman["Portfolio Value"] - kalman["Running Peak"]
    ) / kalman["Running Peak"]

if "Cumulative Return" not in benchmark.columns:
    benchmark["Cumulative Return"] = (
        benchmark["Portfolio Value"] / 100000 - 1
    )

if "Drawdown" not in benchmark.columns:
    benchmark["Running Peak"] = benchmark["Portfolio Value"].cummax()
    benchmark["Drawdown"] = (
        benchmark["Portfolio Value"] - benchmark["Running Peak"]
    ) / benchmark["Running Peak"]

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

page = st.sidebar.radio(
    "Choose Dashboard Section",
    [
        "Overview",
        "Equity Curve",
        "Drawdown",
        "Trade Explorer",
        "Kalman vs OLS",
        "Benchmark Comparison",
        "Parameter Optimization"
    ]
)

# =======================================================
# OVERVIEW
# =======================================================

if page == "Overview":

    st.header("Portfolio Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Final Portfolio Value",
        f"₹{strategy['Portfolio Value'].iloc[-1]:,.2f}"
    )

    col2.metric(
        "Maximum Drawdown",
        f"{abs(strategy['Drawdown'].min())*100:.2f}%"
    )

    col3.metric(
        "Total Trades",
        len(trade_log)
    )

    wins = (trade_log["Return"] > 0).sum()

    col4.metric(
        "Winning Trades",
        wins
    )

    st.divider()

    st.subheader("Portfolio Value")

    fig = px.line(
        strategy,
        x=strategy.index,
        y="Portfolio Value",
        title="Portfolio Value Through Time"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Daily Profit and Loss")

    if "Daily PnL" in strategy.columns:

        pnl_fig = px.line(
            strategy,
            x=strategy.index,
            y="Daily PnL",
            title="Daily PnL"
        )

        st.plotly_chart(pnl_fig, use_container_width=True)

# =======================================================
# EQUITY CURVE
# =======================================================

elif page == "Equity Curve":

    st.header("Equity Curve Analysis")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=strategy.index,
            y=strategy["Portfolio Value"],
            mode="lines",
            name="Strategy"
        )
    )

    fig.update_layout(
        title="Equity Curve",
        xaxis_title="Date",
        yaxis_title="Portfolio Value (₹)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Cumulative Returns")

    cumulative = px.line(
        strategy,
        x=strategy.index,
        y=strategy["Cumulative Return"] * 100,
        title="Cumulative Return (%)"
    )

    st.plotly_chart(cumulative, use_container_width=True)

# =======================================================
# DRAWDOWN
# =======================================================

elif page == "Drawdown":

    st.header("Drawdown Analysis")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=strategy.index,
            y=strategy["Drawdown"] * 100,
            fill="tozeroy",
            mode="lines",
            name="Drawdown"
        )
    )

    fig.update_layout(
        title="Portfolio Drawdown",
        yaxis_title="Drawdown (%)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.metric(
        "Worst Drawdown",
        f"{abs(strategy['Drawdown'].min())*100:.2f}%"
    )

# =======================================================
# TRADE EXPLORER
# =======================================================

elif page == "Trade Explorer":

    st.header("Trade Explorer")

    option = st.selectbox(
        "Filter Trades",
        [
            "All Trades",
            "Winning Trades",
            "Losing Trades"
        ]
    )

    filtered = trade_log.copy()

    if option == "Winning Trades":
        filtered = filtered[filtered["Return"] > 0]

    elif option == "Losing Trades":
        filtered = filtered[filtered["Return"] <= 0]

    st.write(f"Number of Trades: {len(filtered)}")

    st.dataframe(filtered)

    st.subheader("Trade Return Distribution")

    fig = px.histogram(
        filtered,
        x="Return",
        nbins=30,
        title="Trade Returns"
    )

    st.plotly_chart(fig, use_container_width=True)

# =======================================================
# KALMAN VS OLS
# =======================================================

elif page == "Kalman vs OLS":

    st.header("OLS Strategy vs Kalman Filter Strategy")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=strategy.index,
            y=strategy["Portfolio Value"],
            name="OLS Strategy"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=kalman.index,
            y=kalman["Portfolio Value"],
            name="Kalman Strategy"
        )
    )

    fig.update_layout(
        title="Portfolio Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    col1.metric(
        "OLS Final Portfolio",
        f"₹{strategy['Portfolio Value'].iloc[-1]:,.2f}"
    )

    col2.metric(
        "Kalman Final Portfolio",
        f"₹{kalman['Portfolio Value'].iloc[-1]:,.2f}"
    )

# =======================================================
# BENCHMARK
# =======================================================

elif page == "Benchmark Comparison":

    st.header("Strategy vs Buy & Hold Benchmark")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=strategy.index,
            y=strategy["Portfolio Value"],
            name="Statistical Arbitrage"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=benchmark.index,
            y=benchmark["Portfolio Value"],
            name="Buy & Hold"
        )
    )

    fig.update_layout(
        title="Portfolio Value Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Cumulative Returns")

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=strategy.index,
            y=strategy["Cumulative Return"] * 100,
            name="Strategy"
        )
    )

    fig2.add_trace(
        go.Scatter(
            x=benchmark.index,
            y=benchmark["Cumulative Return"] * 100,
            name="Buy & Hold"
        )
    )

    fig2.update_layout(
        title="Cumulative Return Comparison",
        yaxis_title="Return (%)"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Drawdown Comparison")

    fig3 = go.Figure()

    fig3.add_trace(
        go.Scatter(
            x=strategy.index,
            y=strategy["Drawdown"] * 100,
            name="Strategy"
        )
    )

    fig3.add_trace(
        go.Scatter(
            x=benchmark.index,
            y=benchmark["Drawdown"] * 100,
            name="Buy & Hold"
        )
    )

    fig3.update_layout(
        title="Drawdown Comparison"
    )

    st.plotly_chart(fig3, use_container_width=True)

# =======================================================
# PARAMETER OPTIMIZATION
# =======================================================

elif page == "Parameter Optimization":

    st.header("Grid Search Optimization")

    st.subheader("Best Parameters")

    best = optimization.sort_values(
        "Sharpe",
        ascending=False
    ).head(1)

    st.dataframe(best)

    st.subheader("Optimization Results")

    st.dataframe(optimization)

    st.subheader("Sharpe Ratio Heatmap")

    heatmap = optimization.pivot(
        index="Entry Z",
        columns="Exit Z",
        values="Sharpe"
    )

    fig = px.imshow(
        heatmap,
        text_auto=".3f",
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Portfolio Value for Every Parameter Combination")

    fig2 = px.scatter(
        optimization,
        x="Entry Z",
        y="Final Portfolio",
        color="Sharpe",
        size="Trades",
        hover_data=["Exit Z"]
    )

    st.plotly_chart(fig2, use_container_width=True)

st.sidebar.success("Week 8 • Statistical Arbitrage Dashboard")