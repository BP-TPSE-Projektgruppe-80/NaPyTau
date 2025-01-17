import numpy as np
from typing import Tuple


def calculate_tau_final(
    tau_i_values: np.ndarray, delta_tau_i_values: np.ndarray
) -> Tuple[float, float]:
    """
    Computes the final decay time (tau_final) and its associated uncertainty

    Args:
        tau_i_values (ndarray):
        Array of individual decay times (tau_i) for each measurement
        delta_tau_i_values (ndarray):
        Array of uncertainties associated with each tau_i

    Returns:
        tuple: Weighted mean of tau (float) and its uncertainty (float)
    """
    # For empty input arrays return -1 to show the invalidity of the input data.
    if len(tau_i_values) == 0:
        return -1, -1

    weights: np.ndarray = 1 / np.power(delta_tau_i_values, 2)

    # Calculate the weighted mean of tau_i
    weighted_mean: float = np.sum(weights * tau_i_values) / np.sum(weights)

    # Calculate the uncertainty of the weighted mean
    uncertainty: float = np.sqrt(1 / np.sum(weights))

    return weighted_mean, uncertainty
