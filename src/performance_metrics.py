import pandas as pd
import numpy as np

TRADING_DAYS = 252


def annualized_return(strategy_returns):
    cumulative = (1 + strategy_returns).prod()
    periods = len(strategy_returns)

    return cumulative ** (TRADING_DAYS / periods) - 1


def annualized_volatility(strategy_returns):
    return strategy_returns.std() * np.sqrt(TRADING_DAYS)


def sharpe_ratio(strategy_returns, risk_free_rate=0):
    excess = strategy_returns - risk_free_rate / TRADING_DAYS

    return (
        np.sqrt(TRADING_DAYS)
        * excess.mean()
        / excess.std()
    )

def sortino_ratio(strategy_returns):
    downside = strategy_returns[strategy_returns < 0]

    downside_std = downside.std()

    return (
        np.sqrt(TRADING_DAYS)
        * strategy_returns.mean()
        / downside_std
    )

def cagr(results):
    years = len(results) / TRADING_DAYS

    return (
        results["Portfolio Value"].iloc[-1]
        / results["Portfolio Value"].iloc[0]
    ) ** (1 / years) - 1


def calmar_ratio(results):
    max_dd = abs(results["Drawdown"].min())

    return cagr(results) / max_dd

def rolling_sharpe(strategy_returns, window=60):
    return (
        strategy_returns.rolling(window)
        .mean()
        /
        strategy_returns.rolling(window)
        .std()
    ) * np.sqrt(TRADING_DAYS)


def rolling_volatility(strategy_returns, window=60):
    return (
        strategy_returns.rolling(window)
        .std()
        * np.sqrt(TRADING_DAYS)
    )

