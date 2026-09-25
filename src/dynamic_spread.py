import pandas as pd


def create_dynamic_spread(prices, beta):
    spread = (
        prices["INFY"]
        - beta * prices["TCS"]
    )

    spread.name = "Dynamic Spread"

    return spread