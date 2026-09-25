import pandas as pd


def generate_positions_risk_managed(
    signal_series,
    zscore_series,
    stop_loss=3.5,
    take_profit=0.5,
    max_holding_days=20,
):
    position = 0
    holding_days = 0

    positions = []

    for date in signal_series.index:

        signal = signal_series.loc[date]
        z = zscore_series.loc[date]

        if position == 0:

            if signal == 1:
                position = 1
                holding_days = 0

            elif signal == -1:
                position = -1
                holding_days = 0

        else:

            holding_days += 1

            exit_trade = False

            if abs(z) < take_profit:
                exit_trade = True

            elif position == 1 and z < -stop_loss:
                exit_trade = True

            elif position == -1 and z > stop_loss:
                exit_trade = True

            elif holding_days >= max_holding_days:
                exit_trade = True

            if exit_trade:
                position = 0
                holding_days = 0

        positions.append(position)

    return pd.Series(
        positions,
        index=signal_series.index,
    )