from numpy import array
from numpy import sum
from numpy import power
from numpy import zeros


def polynomial_sum_at_measuring_times(times: array, coefficients: array) -> array:
    """
       Computes the sum of a polynomial evaluated at given time points.

       Args:
           times (array): Array of time points where the polynomial is evaluated
           coefficients (array): Array of polynomial coefficients [a_0, a_1, ..., a_n],
                                 where the polynomial is P(t) = a_0 + a_1*t + a_2*t^2 + ... + a_n*t^n.

       Returns:
           array: Array of polynomial values evaluated at the given time points.
    """

    # If no coefficients are provided, return an array of zeros
    if len(coefficients) == 0:
        return zeros(array(len(times)), dtype=float)

    # Evaluate the polynomial sum at the given time points
    return sum(c * power(times, i) for i, c in enumerate(coefficients))


def differentiated_polynomial_sum_at_measuring_times(
    times, coefficients: array
) -> array:
    """
        Computes the sum of the derivative of a polynomial evaluated at given time points.

        Args:
            times (array): Array of time points where the polynomial's derivative is evaluated.
            coefficients (array): Array of polynomial coefficients [a_0, a_1, ..., a_n],
                                  where the polynomial is P(t) = a_0 + a_1*t + a_2*t^2 + ... + a_n*t^n.

        Returns:
            array: Array of the derivative values of the polynomial at the given time points.
        """
    return sum(
        i * c * power(times, (i - 1)) for i, c in enumerate(coefficients) if i > 0
    )
