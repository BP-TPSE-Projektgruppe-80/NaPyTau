from napytau.core.errors.polynomial_coefficient_error import (
    PolynomialCoefficientError,
)
import numpy as np
import scipy as sp
from typing import List

from napytau.core.time import calculate_times_from_distances_and_relative_velocity
from napytau.import_export.model.dataset import DataSet

def evaluate_polynomial_at_measuring_times(
    dataset: DataSet,
    coefficients: np.ndarray,
) -> np.ndarray:
    """
    Computes the sum of a polynomial evaluated at given time points.

    Args:
        dataset (DataSet): The dataset of the experiment
        Datapoints for fitting, consisting of distances and intensities
        coefficients (ndarray):
        Array of polynomial coefficients [a_0, a_1, ..., a_n],
        where the polynomial is P(t) = a_0 + a_1*t + a_2*t^2 + ... + a_n*t^n.

    Returns:
        ndarray: Array of polynomial values evaluated at the given time points.
    """
    if len(coefficients) == 0:
        raise PolynomialCoefficientError(
            "An empty array of coefficients can not be evaluated."
        )

    times: np.ndarray = calculate_times_from_distances_and_relative_velocity(dataset)
    # Evaluate the polynomial sum at the given time points
    sum_at_measuring_distances: np.ndarray = np.zeros_like(times, dtype=float)
    for exponent, coefficient in enumerate(coefficients):
        sum_at_measuring_distances += coefficient * np.power(times, exponent)

    return sum_at_measuring_distances


def evaluate_differentiated_polynomial_at_measuring_times(
    dataset: DataSet,
    coefficients: np.ndarray,
) -> np.ndarray:
    """
    Computes the sum of the derivative of a polynomial evaluated
    at given time points.

    Args:
        dataset (DataSet): The dataset of the experiment
        Datapoints for fitting, consisting of distances and intensities
        coefficients (ndarray):
        Array of polynomial coefficients [a_0, a_1, ..., a_n],
        where the polynomial is P(t) = a_0 + a_1*t + a_2*t^2 + ... + a_n*t^n.

    Returns:
        ndarray:
        Array of the derivative values of the polynomial at the given time points.
    """
    if len(coefficients) == 0:
        raise PolynomialCoefficientError(
            "An empty array of coefficients can not be evaluated."
        )

    times: np.ndarray = calculate_times_from_distances_and_relative_velocity(dataset)
    sum_of_derivative_at_measuring_distances: np.ndarray = np.zeros_like(
        times, dtype=float
    )
    for exponent, coefficient in enumerate(coefficients):
        if exponent > 0:
            sum_of_derivative_at_measuring_distances += (
                exponent * coefficient * np.power(times, (exponent - 1))
            )

    return sum_of_derivative_at_measuring_distances


def calculate_polynomial_coefficients_for_fit(
    dataset: DataSet,
    degree: int,
) -> np.ndarray:
    """
    Calculates the polynomial coefficients for the polynomial fit.

    Args:
        dataset (DataSet): The dataset of the experiment
        degree (int): The degree of the polynomial to be fitted

    Returns:
        ndarray: Array of polynomial coefficients for the fit.
    """
    # Calculate the polynomial coefficients for the fit
    polynomial_coefficients: np.ndarray = (
        np.polynomial.Polynomial.fit(
            calculate_times_from_distances_and_relative_velocity(dataset),
            dataset.get_datapoints().get_shifted_intensities().get_values(),
            degree,
        )
        .convert()
        .coef
    )

    return polynomial_coefficients


def calculate_polynomial_coefficients_for_tau_factor(
    dataset: DataSet,
    tau_factor: float,
    degree: int,
) -> np.ndarray:
    """
    Calculates the polynomial coefficients for the tau factor.

    Args:
        dataset (DataSet): The dataset of the experiment
        tau_factor (float): The tau factor to be used in the polynomial fit
        degree (int): The degree of the polynomial to be fitted

    Returns:
        ndarray: Array of polynomial coefficients for the tau factor.
    """

    polynomial_fit = (
        lambda x, *coefficients: (
            np.poly1d(coefficients)(x) / np.polyder(np.poly1d(coefficients))(x)
        )
        - tau_factor
    )

    # Initial guess: coefficients as ones
    initial_guess = np.ones(degree)

    # Solve for coefficients using least squares
    res = sp.optimize.least_squares(
        lambda coefficients: polynomial_fit(
            calculate_times_from_distances_and_relative_velocity(dataset),
            *coefficients,
        ),
        initial_guess,
    )

    return np.array(res.x)


def calculate_polynomial_coefficients_for_spline_function(
    dataset: DataSet,
    degree: int,
) -> List[np.ndarray]:
    """
        Calculates the polynomial coefficients for the spline function.

        Args:
            dataset (DataSet): The dataset of the experiment
            degree (int): The degree of the polynomials to be fitted

        Returns:
            ndarray: List of arrays of polynomial coefficients for the spline function.
        """
    sampling_points: List[float] = dataset.get_sampling_points()
    measuring_times: np.ndarray = calculate_times_from_distances_and_relative_velocity(dataset)
    intensities: np.ndarray = dataset.get_datapoints().get_shifted_intensities().get_values()

    # Create a mask to assign data points to spaces between sampling points
    bin_indices: np.ndarray = np.digitize(measuring_times, sampling_points)
    sorted_times: List[np.ndarray] = []
    sorted_intensities: List[np.ndarray] = []
    for i in range(len(sampling_points) + 1):
        sorted_times.append(measuring_times[bin_indices == i])
        sorted_intensities.append(intensities[bin_indices == i])

    # Fit polynomial coefficients for each group of data points
    piecewise_polynomial_coefficients: List[np.ndarray] = []
    for i in range(len(sorted_times)):
        polynomial_coefficients: np.ndarray = (
            np.polynomial.Polynomial.fit(
                sorted_times[i],
                sorted_intensities[i],
                degree,
            )
            .convert()
            .coef
        )

        piecewise_polynomial_coefficients.append(polynomial_coefficients)

    return piecewise_polynomial_coefficients


def create_spline_function_from_piecewise_polynomial_coefficients(
    dataset: DataSet,
    piecewise_coefficients: List[np.ndarray],
) -> sp.interpolate.PPoly:
    # Convert to PPoly format: Each row should represent coefficients for one power
    coefficients_matrix: np.ndarray = np.vstack(piecewise_coefficients).T

    # Create piecewise polynomial function
    return sp.interpolate.PPoly(coefficients_matrix, np.array(dataset.get_sampling_points()))
