from numpy import array
from numpy import pow
from numpy import sum
from numpy import sqrt


def calculate_tau_final(tau_i: array, delta_tau_i: array) -> (float, float):
    """
        Computes the final decay time (tau_final) and its associated uncertainty

        Args:
            tau_i (array): Array of individual decay times (tau_i) for each measurement
            delta_tau_i (array): Array of uncertainties associated with each tau_i

        Returns:
            tuple: Weighted mean of tau (float) and its uncertainty (float)
    """
    # Calculate weights based on the inverse square of the uncertainties
    weights: array = 1 / pow(delta_tau_i, 2)

    # Calculate the weighted mean of tau_i
    weighted_mean: float = sum(weights * tau_i) / sum(weights)

    # Calculate the uncertainty of the weighted mean
    uncertainty: float = sqrt(1 / sum(weights))

    # return the weighted mean and its uncertainty as a tuple
    return weighted_mean, uncertainty