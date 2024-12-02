from numpy import array
from numpy import sum
from numpy import power
from numpy import zeros


def polynomial_sum_at_measuring_times(times: array, coefficients: array) -> array:
    if len(coefficients) == 0:
        return zeros(array(len(times)), dtype=float)
    return sum(c * power(times, i) for i, c in enumerate(coefficients))


def differentiated_polynomial_sum_at_measuring_times(
    times, coefficients: array
) -> array:
    return sum(
        i * c * power(times, (i - 1)) for i, c in enumerate(coefficients) if i > 0
    )
