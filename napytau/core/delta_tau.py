from napytau.core.polynomials import differentiated_polynomial_sum_at_measuring_times
from napytau.core.polynomials import polynomial_sum_at_measuring_times
from numpy import array
from numpy import ndarray
from numpy import zeros
from numpy import diag
from numpy import power
from numpy import linalg


def calculate_jacobian_matrix(times: ndarray, coefficients: ndarray) -> ndarray:
    """
    calculated the jacobian matrix for a set of polynomial coefficients taking
    different times into account.
    Adds Disturbances to each coefficient to calculate partial derivatives,
    safes them in jacobian matrix
    Args:
        times (ndarray): Array of time points.
        coefficients (ndarray): Array of polynomial coefficients.

    Returns:
        ndarray:
        The computed Jacobian matrix with shape (len(times), len(coefficients)).
    """

    # initializes the jacobian matrix
    jacobian_matrix: ndarray = zeros((len(times), len(coefficients)))

    epsilon: float = 1e-8  # small disturbance value

    # Loop over each coefficient and calculate the partial derivative
    for i in range(len(coefficients)):
        perturbed_coefficients: ndarray = array(coefficients, dtype=float)
        perturbed_coefficients[i] += epsilon  # slightly disturb the current coefficient

        # Compute the disturbed and original polynomial values at the given times
        perturbed_function: ndarray = polynomial_sum_at_measuring_times(
            times, perturbed_coefficients
        )
        original_function: ndarray = polynomial_sum_at_measuring_times(
            times, coefficients
        )

        # Calculate the partial derivative coefficients and store it in the
        # Jacobian matrix
        jacobian_matrix[:, i] = (perturbed_function - original_function) / epsilon

    return jacobian_matrix


def calculate_covariance_matrix(
    delta_shifted_intensities: ndarray, times: ndarray, coefficients: ndarray
) -> ndarray:
    """
    Computes the covariance matrix for the polynomial coefficients using the
    jacobian matrix and a weight matrix derived from the shifted intensities' errors.
    Args:
        delta_shifted_intensities (ndarray): Errors in the shifted intensities.
        times (ndarray): Array of time points.
        coefficients (ndarray): Array of polynomial coefficients.

    Returns:
        ndarray: The computed covariance matrix for the polynomial coefficients.
    """

    # Compute the Jacobian matrix for the polynomial
    jacobian_matrix: ndarray = calculate_jacobian_matrix(times, coefficients)

    # Construct the weight matrix from the inverse squared errors
    weight_matrix: ndarray = diag(1 / power(delta_shifted_intensities, 2))

    # Compute the fit matrix
    fit_matrix: ndarray = jacobian_matrix.T @ weight_matrix @ jacobian_matrix

    # Invert the fit matrix to get the covariance matrix
    covariance_matrix: ndarray = linalg.inv(fit_matrix)

    return covariance_matrix


def calculate_error_propagation_terms(
    unshifted_intensities: ndarray,
    delta_shifted_intensities: ndarray,
    delta_unshifted_intensities: ndarray,
    times: ndarray,
    coefficients: ndarray,
    taufactor: float,
) -> ndarray:
    """
    creates the gaussian error propagation term for the polynomial coefficients.
    combining direct errors, polynomial uncertainties, and mixed covariance terms.
    Args:
        unshifted_intensities (ndarray): Unshifted intensity values.
        delta_shifted_intensities (ndarray): Errors in the shifted intensities.
        delta_unshifted_intensities (ndarray): Errors in the unshifted intensities.
        times (ndarray): Array of time points.
        coefficients (ndarray): Array of polynomial coefficients.
        taufactor (float): Scaling factor related to the Doppler-shift model.

    Returns:
        ndarray: The combined Gaussian error propagation terms for each time point.
    """

    calculated_differentiated_polynomial_sum_at_measuring_times = (
        differentiated_polynomial_sum_at_measuring_times(  # noqa E501
            times,
            coefficients,
        )
    )

    # First summand: Contribution from unshifted intensity errors
    first_summand: ndarray = power(delta_unshifted_intensities, 2) / power(
        calculated_differentiated_polynomial_sum_at_measuring_times,
        2,
    )

    # Initialize the polynomial uncertainty term for second term
    delta_p_j_i_squared: ndarray = zeros(len(times))
    covariance_matrix: ndarray = calculate_covariance_matrix(
        delta_shifted_intensities, times, coefficients
    )

    # Calculate the polynomial uncertainty contributions
    for k in range(len(coefficients)):
        for l in range(len(coefficients)):  # noqa E741
            delta_p_j_i_squared = (
                delta_p_j_i_squared
                + power(times, k) * power(times, l) * covariance_matrix[k, l]
            )

    # Second summand: Contribution from polynomial uncertainties
    second_summand: ndarray = (
        power(unshifted_intensities, 2)
        / power(
            calculated_differentiated_polynomial_sum_at_measuring_times,
            4,
        )
    ) * power(delta_p_j_i_squared, 2)

    # Third summand: Mixed covariance contribution
    third_summand: ndarray = (
        unshifted_intensities * taufactor * delta_p_j_i_squared
    ) / power(calculated_differentiated_polynomial_sum_at_measuring_times, 3)

    # Return the sum of all three contribution
    result: ndarray = first_summand + second_summand + third_summand

    return result