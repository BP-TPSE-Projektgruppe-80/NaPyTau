from numpy import array
from numpy import pow
from numpy import sum
from numpy import sqrt


def calculate_tau_final(tau_i: array, delta_tau_i: array) -> (float, float):
    weights: array = 1 / pow(delta_tau_i, 2)

    weighted_mean: float = sum(weights * tau_i) / sum(weights)
    uncertainty: float = sqrt(1 / sum(weights))

    return weighted_mean, uncertainty