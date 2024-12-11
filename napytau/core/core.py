from numpy import ndarray
from numpy import pow
from numpy import sum
from numpy import sqrt
from typing import Tuple


def calculate_tau_final(tau_i: ndarray, delta_tau_i: ndarray) -> Tuple[float, float]:
    """
        Computes the final decay time (tau_final) and its associated uncertainty

        Args:
            tau_i (ndarray):
            Array of individual decay times (tau_i) for each measurement
            delta_tau_i (ndarray):
            Array of uncertainties associated with each tau_i

        Returns:
            tuple: Weighted mean of tau (float) and its uncertainty (float)
    """
    # Calculate weights based on the inverse square of the uncertainties
    weights: ndarray = 1 / pow(delta_tau_i, 2)

    # Calculate the weighted mean of tau_i
    weighted_mean: float = sum(weights * tau_i) / sum(weights)

    # Calculate the uncertainty of the weighted mean
    uncertainty: float = sqrt(1 / sum(weights))

    # Edge case handling for empty input array
    if tau_i.size == 0:
        return -1, -1

    # return the weighted mean and its uncertainty as a tuple
    return weighted_mean, uncertainty