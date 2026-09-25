import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from src.data_loader import load_stock
from src.cointegration import engle_granger_test
from src.hedge_ratio import calculate_hedge_ratio

tcs = load_stock("TCS.NS")
infy = load_stock("INFY.NS")

prices = pd.concat(
    [tcs["Close"], infy["Close"]],
    axis=1
)

prices.columns = ["TCS", "INFY"]
#calculate hedge ratio for TCS and INFY

alpha, beta, model = calculate_hedge_ratio(
    prices["TCS"],
    prices["INFY"]
)

print("Alpha:", alpha)
print("Beta :", beta)

#run cointegration test for TCS and INFY
result = engle_granger_test(
    prices["TCS"],
    prices["INFY"],
    "TCS-INFY"
)

print(result)

#compute spread for TCS and INFY
spread = prices["INFY"] - beta * prices["TCS"]
print("Spread:")
print(spread)

#test spread stationarity using ADF test
from src.stationarity import print_adf

print_adf(spread, "TCS-INFY Spread")

#generate every pair
from itertools import combinations
from src.config import NIFTY_STOCKS

pairs = list(combinations(NIFTY_STOCKS, 2))

#loop through pairs
results = []

for stock1, stock2 in pairs:

    df1 = load_stock(stock1)
    df2 = load_stock(stock2)

    merged = pd.concat(
        [df1["Close"], df2["Close"]],
        axis=1
    ).dropna()

    merged.columns = ["A", "B"]

    result = engle_granger_test(
        merged["A"],
        merged["B"],
        f"{stock1}-{stock2}"
    )

    results.append(result)
results_df = pd.DataFrame(results)
cointegrated = results_df[results_df["P-value"] < 0.05]

print(cointegrated)
cointegrated.to_csv(
    "results/tables/cointegrated_pairs.csv",
    index=False
)

#plot spread
import matplotlib.pyplot as plt

plt.figure(figsize=(12,5))

plt.plot(spread)

plt.axhline(spread.mean(), color="red", linestyle="--")

plt.title("TCS-INFY Spread")

plt.savefig("results/figures/tcs_infy_spread.png")

plt.close()

#z-score of spread
spread_mean = spread.mean()
spread_std = spread.std()

zscore = (spread - spread_mean) / spread_std

#plot z-score
plt.figure(figsize=(12,5))

plt.plot(zscore)

plt.axhline(2, linestyle="--", color="red")
plt.axhline(-2, linestyle="--", color="green")
plt.axhline(0, linestyle="--", color="black")

plt.title("Spread Z-score")

plt.savefig("results/figures/zscore_tcs_infy.png")

plt.close()