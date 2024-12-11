from numpy import ndarray
from numpy import array
from numpy import power
from numpy import zeros
from numpy import zeros_like


def polynomial_sum_at_measuring_times(times: ndarray, coefficients: ndarray) -> ndarray:
    """
       Computes the sum of a polynomial evaluated at given time points.

       Args:
           times (ndarray):
           Array of time points where the polynomial is evaluated
           coefficients (ndarray):
           Array of polynomial coefficients [a_0, a_1, ..., a_n],
           where the polynomial is P(t) = a_0 + a_1*t + a_2*t^2 + ... + a_n*t^n.

       Returns:
           ndarray: Array of polynomial values evaluated at the given time points.
    """

    # If no coefficients are provided, return a ndarray of zeros
    if len(coefficients) == 0:
        return zeros(array(len(times)), dtype=float)

    # Evaluate the polynomial sum at the given time points
    result: ndarray = zeros_like(times)
    for i, c in enumerate(coefficients):
        result += c * power(times, i)
    return result


def differentiated_polynomial_sum_at_measuring_times(
    times: ndarray, coefficients: ndarray
) -> ndarray:
    """
        Computes the sum of the derivative of a polynomial evaluated
        at given time points.

        Args:
            times (ndarray):
            Array of time points where the polynomial's derivative is evaluated.
            coefficients (ndarray):
            Array of polynomial coefficients [a_0, a_1, ..., a_n],
            where the polynomial is P(t) = a_0 + a_1*t + a_2*t^2 + ... + a_n*t^n.

        Returns:
            ndarray:
            Array of the derivative values of the polynomial at the given time points.
        """
    result: ndarray = zeros_like(times)
    for i, c in enumerate(coefficients):
        if i > 0:
            result += i * c * power(times, (i - 1))
    return result
