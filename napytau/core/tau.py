from numpy import poly1d
from polynomials import differentiate_polynomial
from polynomials import get_polynomial
from polynomials import determine_coefficients

def calculate_tau(doppler_shifted_intensities: list[float],
                  unshifted_intensities: list[float],
                  distances: list[float], power: int) -> list[float]:
    tau_list : list[float] = []
    for i in range(len(distances) - 1):
        coefficients: list[float] = (
            list(determine_coefficients(unshifted_intensities, distances)))
        tau_i = (doppler_shifted_intensities[i] / differentiate_polynomial(
            get_polynomial(coefficients[0], coefficients[1],
                           coefficients[2]))(i))
        tau_list.append(tau_i)
    return tau_list