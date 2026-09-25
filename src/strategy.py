import pandas as pd


def generate_positions(signals):
    """
    Convert entry signals into held positions.
    """

    position = 0

    positions = []

    for signal in signals:

        if signal == 1 and position == 0:
            position = 1

        elif signal == -1 and position == 0:
            position = -1

        elif signal == 0:
            position = 0

        positions.append(position)

    return positions