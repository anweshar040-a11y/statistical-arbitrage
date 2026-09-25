import statsmodels.api as sm


def calculate_hedge_ratio(x, y):
    """
    Estimate hedge ratio using Ordinary Least Squares.
    """

    X = sm.add_constant(x)

    model = sm.OLS(y, X).fit()

    alpha = model.params.iloc[0]
    beta = model.params.iloc[1]

    return alpha, beta, model