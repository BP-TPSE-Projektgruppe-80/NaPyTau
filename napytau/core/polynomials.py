from napytau.core.errors.polynomial_coefficient_error import (
    PolynomialCoefficientError,
)
import numpy as np
import scipy as sp

from napytau.import_export.model.dataset import DataSet


def _calculate_times_from_distances_and_relative_velocity(
    dataset: DataSet,
) -> np.ndarray:
    return np.array(
        dataset.get_datapoints().get_distances().get_values()
        / (
            dataset.get_relative_velocity().value.get_velocity()
            * sp.constants.speed_of_light
        )
    )


def evaluate_polynomial_at_measuring_distances(
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

    times: np.ndarray = _calculate_times_from_distances_and_relative_velocity(dataset)
    # Evaluate the polynomial sum at the given time points
    sum_at_measuring_distances: np.ndarray = np.zeros_like(times, dtype=float)
    for exponent, coefficient in enumerate(coefficients):
        sum_at_measuring_distances += coefficient * np.power(times, exponent)

    return sum_at_measuring_distances


def evaluate_differentiated_polynomial_at_measuring_distances(
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

    times: np.ndarray = _calculate_times_from_distances_and_relative_velocity(dataset)
    sum_of_derivative_at_measuring_distances: np.ndarray = np.zeros_like(
        times, dtype=float
    )
    for exponent, coefficient in enumerate(coefficients):
        if exponent > 0:
            sum_of_derivative_at_measuring_distances += (
                exponent * coefficient * np.power(times, (exponent - 1))
            )

    return sum_of_derivative_at_measuring_distances


def calculate_polynomial_coefficients_for_fit(dataset: DataSet) -> np.ndarray:
    """
    Calculates the polynomial coefficients for the polynomial fit.

    Args:
        dataset (DataSet): The dataset of the experiment

    Returns:
        ndarray: Array of polynomial coefficients for the fit.
    """
    # Calculate the polynomial coefficients for the fit
    polynomial_coefficients: np.ndarray = (
        np.polynomial.Polynomial.fit(
            dataset.get_datapoints().get_distances().get_values(),
            dataset.get_datapoints().get_shifted_intensities().get_values(),
            dataset.get_polynomial_degree(),
        )
        .convert()
        .coef
    )

    return polynomial_coefficients


def calculate_polynomial_coefficients_for_tau_factor(
    dataset: DataSet,
    tau_factor: float,
) -> np.ndarray:
    """
    Calculates the polynomial coefficients for the tau factor.

    Args:
        dataset (DataSet): The dataset of the experiment
        tau_factor (float): The tau factor to be used in the polynomial fit

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
    initial_guess = np.ones(dataset.get_polynomial_degree() + 1)

    # Solve for coefficients using least squares
    res = sp.least_squares(
        lambda coefficients: polynomial_fit(
            dataset.get_datapoints().get_distances().get_values(),
            *coefficients,
        ),
        initial_guess,
    )

    return np.array(res.x)
