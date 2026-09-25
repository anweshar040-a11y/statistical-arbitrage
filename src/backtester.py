import pandas as pd


def backtest_strategy(prices, signals, beta):
    data = prices.copy()

    data["Signal"] = signals["Signal"]
    data["Position"] = signals["Position"]

    data["Spread Change"] = data["Spread"].diff().fillna(0)

    data["Hedge Value"] = (
        data["INFY"].abs()
        + abs(beta) * data["TCS"].abs()
    )

    data["Spread Return"] = (
        data["Spread Change"] / data["Hedge Value"]
    ).fillna(0)

    data["Strategy Return"] = (
        data["Position"]
        .shift(1)
        .fillna(0)
        * data["Spread Return"]
    )

    transaction_cost = 0.0005

    trade_change = (
        data["Position"]
        .diff()
        .abs()
        .fillna(0)
    )

    data["Transaction Cost"] = (
        trade_change * transaction_cost
    )

    data["Strategy Return"] = (
        data["Strategy Return"]
        - data["Transaction Cost"]
    )

    return data


def create_trade_log(data):
    trades = []

    current_trade = None

    for date, row in data.iterrows():

        if current_trade is None:

            if row["Position"] != 0:

                current_trade = {
                    "Entry Date": date,
                    "Direction": (
                        "Long"
                        if row["Position"] == 1
                        else "Short"
                    ),
                    "Entry Spread": row["Spread"],
                }

        else:

            if row["Position"] == 0:

                current_trade["Exit Date"] = date
                current_trade["Exit Spread"] = row["Spread"]

                entry = current_trade["Entry Spread"]
                exit_price = current_trade["Exit Spread"]

                if current_trade["Direction"] == "Long":

                    pnl = (
                        exit_price - entry
                    ) / abs(entry)

                else:

                    pnl = (
                        entry - exit_price
                    ) / abs(entry)

                current_trade["Return"] = pnl

                trades.append(current_trade)

                current_trade = None

    return pd.DataFrame(trades)