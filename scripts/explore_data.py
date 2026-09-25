import sys
from pathlib import Path
import matplotlib.pyplot as plt

# Tell Python where the project root is
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from src.data_loader import load_stock
from src.visualization import plot_prices

tcs = load_stock("TCS.NS")
infy = load_stock("INFY.NS")

prices = pd.concat(
    [tcs["Close"], infy["Close"]],
    axis=1
)

prices.columns = ["TCS", "INFY"]

plot_prices(
    prices,
    "TCS vs Infosys Prices",
    "results/figures/prices.png"
)

print(prices.head())
print(prices.describe())
#returns

returns = prices.pct_change().dropna()

plot_prices(
    returns,
    "Daily Returns",
    "results/figures/daily_returns.png"
)


plt.figure(figsize=(8,5))
returns["TCS"].hist(bins=50)

plt.title("Distribution of TCS Daily Returns")
plt.tight_layout()
plt.savefig("results/figures/tcs_return_histogram.png")
plt.close()

normalized = prices / prices.iloc[0]

plot_prices(
    normalized,
    "Normalized Prices",
    "results/figures/normalized_prices.png"
)

print("Missing values:")
print(prices.isna().sum())

print("\nCorrelation:")
print(prices.corr())

print("\nDaily Return Statistics:")
print(returns.describe())

import matplotlib.pyplot as plt

plt.figure(figsize=(5,4))
plt.imshow(prices.corr(), cmap="coolwarm")

plt.xticks([0,1], prices.columns)
plt.yticks([0,1], prices.columns)

plt.colorbar()
plt.title("Correlation Matrix")

plt.savefig("results/figures/correlation_heatmap.png")
plt.close()
#week 1 ends here