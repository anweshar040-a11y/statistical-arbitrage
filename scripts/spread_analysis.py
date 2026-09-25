import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import load_stock
from src.hedge_ratio import calculate_hedge_ratio
from src.statistics_utils import rolling_zscore
from src.strategy import generate_positions
tcs = load_stock("TCS.NS")
infy = load_stock("INFY.NS")

prices = pd.concat([tcs["Close"], infy["Close"]], axis=1).dropna()
prices.columns = ["TCS", "INFY"]

alpha, beta, model = calculate_hedge_ratio(
    prices["TCS"],
    prices["INFY"]
)

print(f"Hedge Ratio (Beta): {beta:.4f}")

spread = prices["INFY"] - beta * prices["TCS"]

zscore = rolling_zscore(spread)

plt.figure(figsize=(12, 5))
plt.plot(spread, label="Spread")
plt.axhline(spread.mean(), color="red", linestyle="--", label="Mean")
plt.title("TCS-INFY Spread")
plt.xlabel("Date")
plt.ylabel("Spread")
plt.legend()
plt.tight_layout()
plt.savefig("results/figures/tcs_infy_spread.png")
plt.close()

plt.figure(figsize=(12, 5))
plt.plot(zscore, label="Rolling Z-Score")
plt.axhline(2, color="red", linestyle="--", label="+2")
plt.axhline(-2, color="green", linestyle="--", label="-2")
plt.axhline(0, color="black", linestyle="--", label="Mean")
plt.title("Rolling Z-Score of TCS-INFY Spread")
plt.xlabel("Date")
plt.ylabel("Z-Score")
plt.legend()
plt.tight_layout()
plt.savefig("results/figures/rolling_zscore.png")
plt.close()

print("Plots saved successfully.")


#BUILD SIGNAL GENERATOR
signals = pd.DataFrame(index=zscore.index)

signals["Z-Score"] = zscore
signals["Signal"] = 0

#ENTRY SIGNALS
signals.loc[zscore > 2, "Signal"] = -1
signals.loc[zscore < -2, "Signal"] = 1


#EXIT SIGNALS
signals.loc[abs(zscore) < 0.5, "Signal"] = 0
signals.loc[zscore > 3, "Signal"] = 0
signals.loc[zscore < -3, "Signal"] = 0

signals.to_csv(
    "results/tables/signal_log.csv"
)

signals["Position"] = generate_positions(
    signals["Signal"]
)

#TRADING LOG
trades = []

current_trade = None
for date, row in signals.iterrows():

    if current_trade is None:

        if row["Position"] != 0:

            current_trade = {
                "Entry Date": date,
                "Direction": row["Position"],
                "Entry Z": row["Z-Score"]
            }

    else:

        if row["Position"] == 0:

            current_trade["Exit Date"] = date
            current_trade["Exit Z"] = row["Z-Score"]

            trades.append(current_trade)

            current_trade = None

trade_log = pd.DataFrame(trades)

trade_log.to_csv(
    "results/tables/trade_log.csv",
    index=False
)

#plot buy and sell signals
plt.figure(figsize=(14,6))

plt.plot(spread, label="Spread")

buy = signals["Signal"] == 1
sell = signals["Signal"] == -1

plt.scatter(
    spread.index[buy],
    spread[buy],
    marker="^",
    label="Long",
    s=80
)

plt.scatter(
    spread.index[sell],
    spread[sell],
    marker="v",
    label="Short",
    s=80
)

plt.legend()

plt.savefig("results/figures/spread_signals.png")

plt.close()
#plot zscore signals

plt.figure(figsize=(14,5))

plt.plot(zscore)

plt.scatter(
    zscore.index[buy],
    zscore[buy],
    marker="^",
    s=70
)

plt.scatter(
    zscore.index[sell],
    zscore[sell],
    marker="v",
    s=70
)

plt.axhline(2, linestyle="--")
plt.axhline(-2, linestyle="--")
plt.axhline(0)

plt.savefig("results/figures/zscore_signals.png")

plt.close()