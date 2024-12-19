from numpy import ndarray
from numpy import power
from numpy import zeros_like

from napytau.core.errors.polynomial_coefficient_error import (
    PolynomialCoefficientError,
)


def evaluate_polynomial_at_measuring_distances(
    distances: ndarray, coefficients: ndarray
) -> ndarray:
    """
    Computes the sum of a polynomial evaluated at given distance points.

    Args:
        distances (ndarray):
        Array of distance points where the polynomial is evaluated
        coefficients (ndarray):
        Array of polynomial coefficients [a_0, a_1, ..., a_n],
        where the polynomial is P(t) = a_0 + a_1*t + a_2*t^2 + ... + a_n*t^n.

    Returns:
        ndarray: Array of polynomial values evaluated at the given distance points.
    """
    if len(coefficients) == 0:
        raise PolynomialCoefficientError(
            "An empty array of coefficients can not be evaluated."
        )

    # Evaluate the polynomial sum at the given time points
    sum_at_measuring_distances: ndarray = zeros_like(distances, dtype=float)
    for exponent, coefficient in enumerate(coefficients):
        sum_at_measuring_distances += coefficient * power(distances, exponent)

    return sum_at_measuring_distances


def evaluate_differentiated_polynomial_at_measuring_distances(
    distances: ndarray, coefficients: ndarray
) -> ndarray:
    """
    Computes the sum of the derivative of a polynomial evaluated
    at given distance points.

    Args:
        distances (ndarray):
        Array of distance points where the polynomial's derivative is evaluated.
        coefficients (ndarray):
        Array of polynomial coefficients [a_0, a_1, ..., a_n],
        where the polynomial is P(t) = a_0 + a_1*t + a_2*t^2 + ... + a_n*t^n.

    Returns:
        ndarray:
        Array of the derivative values of the polynomial at the given distance points.
    """
    if len(coefficients) == 0:
        raise PolynomialCoefficientError(
            "An empty array of coefficients can not be evaluated."
        )

    sum_of_derivative_at_measuring_distances: ndarray = zeros_like(
        distances, dtype=float
    )
    for exponent, coefficient in enumerate(coefficients):
        if exponent > 0:
            sum_of_derivative_at_measuring_distances += (
                exponent * coefficient * power(distances, (exponent - 1))
            )

    return sum_of_derivative_at_measuring_distances
