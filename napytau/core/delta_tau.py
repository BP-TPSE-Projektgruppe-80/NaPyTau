from napytau.core.polynomials import differentiated_polynomial_sum_at_measuring_times
from napytau.core.polynomials import polynomial_sum_at_measuring_times
from numpy import array
from numpy import ndarray
from numpy import zeros
from numpy import diag
from numpy import power
from numpy import linalg


def calculate_jacobian_matrix(times: array, coefficients: array) -> ndarray:
    jacobian_matrix: ndarray = zeros((len(times), len(coefficients)))

    epsilon: float = 1e-8
    for i in range(len(coefficients)):
        perturbed_coefficients: array = array(coefficients, dtype=float)
        perturbed_coefficients[i] += epsilon
        perturbed_function: array = polynomial_sum_at_measuring_times(
            times, perturbed_coefficients
        )
        original_function: array = polynomial_sum_at_measuring_times(
            times, coefficients
        )
        jacobian_matrix[:, i] = (perturbed_function - original_function) / epsilon

    return jacobian_matrix


def calculate_covariance_matrix(
    delta_shifted_intensities: array, times: array, coefficients: array
) -> ndarray:
    # Compute the Jacobian Matrix
    jacobian_matrix: ndarray = calculate_jacobian_matrix(times, coefficients)
    # Construct the weight matrix using the errors
    weight_matrix: ndarray = diag(1 / power(delta_shifted_intensities, 2))
    # Compute the fit matrix
    fit_matrix: ndarray = jacobian_matrix.T @ weight_matrix @ jacobian_matrix
    # Invert the fit matrix to get the covariance matrix
    covariance_matrix: ndarray = linalg.inv(fit_matrix)

    return covariance_matrix


def calculate_gaussian_error_propagation_terms(
    unshifted_intensities: array,
    delta_shifted_intensities: array,
    delta_unshifted_intensities: array,
    times: array,
    coefficients: array,
    taufactor: float,
    ) -> array:
    first_summand: array = power(delta_unshifted_intensities, 2) / power(
        differentiated_polynomial_sum_at_measuring_times(
            times,
            coefficients,
        ),
        2,
    )

    delta_p_j_i_squared: array = zeros(len(times))
    covariance_matrix: ndarray = calculate_covariance_matrix(
        delta_shifted_intensities, times, coefficients
    )
    for k in range(len(coefficients)):
        for l in range(len(coefficients)):  # noqa E741
            delta_p_j_i_squared = sum(
                delta_p_j_i_squared,
                power(times, k) * power(times, l) * covariance_matrix[k, l],
            )

    second_summand: array = (
        power(unshifted_intensities, 2)
        / power(
            differentiated_polynomial_sum_at_measuring_times(
                times,
                coefficients,
            ),
            4,
        )
    ) * power(delta_p_j_i_squared, 2)

    third_summand: array = \
        ((unshifted_intensities * taufactor * delta_p_j_i_squared)
         / power(differentiated_polynomial_sum_at_measuring_times(
                    times,
                    coefficients), 3))

    return first_summand + second_summand + third_summand