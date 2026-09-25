from statsmodels.tsa.stattools import coint


def engle_granger_test(series1, series2, pair_name="Pair"):
    """
    Perform Engle-Granger Cointegration Test.
    """

    score, pvalue, critical_values = coint(series1, series2)

    return {
        "Pair": pair_name,
        "Test Statistic": score,
        "P-value": pvalue,
        "Critical Values": critical_values
    }