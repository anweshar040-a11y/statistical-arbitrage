from statsmodels.tsa.stattools import adfuller
import pandas as pd


def adf_test(series, title="Series"):
    """
    Perform Augmented Dickey-Fuller Test and return results.
    """

    series = series.dropna()

    # CHANGED: added result_object=False to remove FutureWarning
    result = adfuller(series, result_object=False)

    output = {
        "Series": title,
        "ADF Statistic": result[0],
        "p-value": result[1],
        "Lags Used": result[2],
        "Observations": result[3],
        "Critical Values": result[4]      # CHANGED: added this key
    }

    return output


def print_adf(series, title="Series"):
    """
    Prints ADF results in a readable format.
    """

    output = adf_test(series, title)

    print("=" * 50)
    print(output["Series"])
    print("=" * 50)

    print(f"ADF Statistic : {output['ADF Statistic']:.4f}")
    print(f"P-value       : {output['p-value']:.6f}")
    print(f"Lags Used     : {output['Lags Used']}")
    print(f"Observations  : {output['Observations']}")

    print("\nCritical Values")
    for key, value in output["Critical Values"].items():
        print(f"{key}: {value:.4f}")

    if output["p-value"] < 0.05:
        print("\nConclusion: Stationary ✅ (Reject Null Hypothesis)")
    else:
        print("\nConclusion: Non-Stationary ❌ (Cannot Reject Null Hypothesis)")