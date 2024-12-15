from numpy import ndarray
from numpy import array
from numpy import power
from numpy import zeros
from numpy import zeros_like


def polynomial_sum_at_measuring_distances(distances: ndarray, coefficients: ndarray) -> ndarray:
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

    # If no coefficients are provided, return a ndarray of zeros
    if len(coefficients) == 0:
        return zeros(array(len(distances)), dtype=float)

    # Evaluate the polynomial sum at the given time points
    result: ndarray = zeros_like(distances)
    for i, c in enumerate(coefficients):
        result += c * power(distances, i)
    return result


def differentiated_polynomial_sum_at_measuring_distances(
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
    result: ndarray = zeros_like(distances)
    for i, c in enumerate(coefficients):
        if i > 0:
            result += i * c * power(distances, (i - 1))
    return result
