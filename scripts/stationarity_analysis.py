import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_stock
from src.stationarity import adf_test, print_adf

tcs = load_stock("TCS.NS")

price_result = adf_test(tcs["Close"], "TCS Closing Price")
returns = tcs["Close"].pct_change()

return_result = adf_test(
    returns,
    "TCS Daily Returns"
)

print(price_result)
print(return_result)


#testing multiple stocks

from src.config import NIFTY_STOCKS
from src.data_loader import load_stock
results = []

for stock in NIFTY_STOCKS:

    df = load_stock(stock)
    returns = df["Close"].pct_change()

    # -------- Price ADF --------
    print_adf(df["Close"], f"{stock} Closing Price")
    print()

    # -------- Returns ADF --------
    print_adf(returns, f"{stock} Daily Returns")
    print()

    # Save results for DataFrame (Price)
    results.append(adf_test(df["Close"], f"{stock} Closing Price"))

    # Save results for DataFrame (Returns)
    results.append(adf_test(returns, f"{stock} Daily Returns"))
import pandas as pd

results_df = pd.DataFrame(results)

print(results_df)

results_df.to_csv(
    "results/tables/adf_results.csv",
    index=False
)
#compare prices and returns for multiple stocks
import matplotlib.pyplot as plt

fig, ax = plt.subplots(2,1, figsize=(12,8))

ax[0].plot(tcs["Close"])
ax[0].set_title("TCS Closing Price")

ax[1].plot(returns)
ax[1].set_title("TCS Daily Returns")

plt.tight_layout()
plt.savefig("results/figures/stationarity_price_vs_return.png")
plt.close()

#rolling mean and rolling std
rolling_mean = returns.rolling(window=30).mean()
rolling_std = returns.rolling(window=30).std()

plt.figure(figsize=(12,5))

plt.plot(returns, alpha=0.5, label="Returns")
plt.plot(rolling_mean, label="30-Day Mean")
plt.plot(rolling_std, label="30-Day Std")

plt.legend()
plt.title("Rolling Statistics")

plt.savefig("results/figures/rolling_statistics.png")
plt.close()