import pandas as pd
import numpy as np
from pykalman import KalmanFilter


def kalman_hedge_ratio(x, y):
    index = x.index

    observation_matrix = x.values.reshape(-1, 1, 1)
    observations = y.values

    kf = KalmanFilter(
        transition_matrices=np.array([[1.0]]),
        observation_matrices=observation_matrix,
        initial_state_mean=np.array([1.0]),
        initial_state_covariance=np.array([[1.0]]),
        observation_covariance=np.array([[1.0]]),
        transition_covariance=np.array([[0.001]])
    )

    state_means, _ = kf.filter(observations)

    return pd.Series(
        state_means.flatten(),
        index=index,
        name="Kalman Beta"
    )