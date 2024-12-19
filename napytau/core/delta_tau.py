from napytau.core.polynomials import evaluate_differentiated_polynomial_at_measuring_distances # noqa E501
from napytau.core.polynomials import evaluate_polynomial_at_measuring_distances
from numpy import array
from numpy import ndarray
from numpy import zeros
from numpy import diag
from numpy import power
from numpy import linalg


def calculate_jacobian_matrix(distances: ndarray, coefficients: ndarray) -> ndarray:
    """
    calculated the jacobian matrix for a set of polynomial coefficients taking
    different distances into account.
    Adds Disturbances to each coefficient to calculate partial derivatives,
    safes them in jacobian matrix
    Args:
        distances (ndarray): Array of distance points.
        coefficients (ndarray): Array of polynomial coefficients.

    Returns:
        ndarray:
        The computed Jacobian matrix with shape (len(distances), len(coefficients)).
    """

    # initializes the jacobian matrix
    jacobian_matrix: ndarray = zeros((len(distances), len(coefficients)))

    epsilon: float = 1e-8  # small disturbance value

    # Loop over each coefficient and calculate the partial derivative
    for i in range(len(coefficients)):
        perturbed_coefficients: ndarray = array(coefficients, dtype=float)
        perturbed_coefficients[i] += epsilon  # slightly disturb the current coefficient

        # Compute the disturbed and original polynomial values at the given distances
        perturbed_function: ndarray = evaluate_polynomial_at_measuring_distances(
            distances, perturbed_coefficients
        )
        original_function: ndarray = evaluate_polynomial_at_measuring_distances(
            distances, coefficients
        )

        # Calculate the partial derivative coefficients and store it in the
        # Jacobian matrix
        # jacobian_matrix[:, i] selects the entire column i of the jacobian matrix
        # The colon (:) indicates all rows and i specifies the column
        jacobian_matrix[:, i] = (perturbed_function - original_function) / epsilon

    return jacobian_matrix


def calculate_covariance_matrix(
    delta_shifted_intensities: ndarray, distances: ndarray, coefficients: ndarray
) -> ndarray:
    """
    Computes the covariance matrix for the polynomial coefficients using the
    jacobian matrix and a weight matrix derived from the shifted intensities' errors.
    Args:
        delta_shifted_intensities (ndarray): Errors in the shifted intensities.
        distances (ndarray): Array of distance points.
        coefficients (ndarray): Array of polynomial coefficients.

    Returns:
        ndarray: The computed covariance matrix for the polynomial coefficients.
    """

    jacobian_matrix: ndarray = calculate_jacobian_matrix(distances, coefficients)

    # Construct the weight matrix from the inverse squared errors
    weight_matrix: ndarray = diag(1 / power(delta_shifted_intensities, 2))

    fit_matrix: ndarray = jacobian_matrix.T @ weight_matrix @ jacobian_matrix

    covariance_matrix: ndarray = linalg.inv(fit_matrix)

    return covariance_matrix


def calculate_error_propagation_terms(
    unshifted_intensities: ndarray,
    delta_shifted_intensities: ndarray,
    delta_unshifted_intensities: ndarray,
    distances: ndarray,
    coefficients: ndarray,
    taufactor: float,
) -> ndarray:
    """
    creates the error propagation term for the polynomial coefficients.
    combining direct errors, polynomial uncertainties, and mixed covariance terms.
    Args:
        unshifted_intensities (ndarray): Unshifted intensity values.
        delta_shifted_intensities (ndarray): Errors in the shifted intensities.
        delta_unshifted_intensities (ndarray): Errors in the unshifted intensities.
        distances (ndarray): Array of distance points.
        coefficients (ndarray): Array of polynomial coefficients.
        taufactor (float): Scaling factor related to the Doppler-shift model.

    Returns:
        ndarray: The combined error propagation terms for each distance point.
    """

    calculated_differentiated_polynomial_sum_at_measuring_distances = (
        evaluate_differentiated_polynomial_at_measuring_distances(  # noqa E501
            distances,
            coefficients,
        )
    )

    gaussian_error_from_unshifted_intensity: ndarray = power(delta_unshifted_intensities, 2) / power(
        calculated_differentiated_polynomial_sum_at_measuring_distances,
        2,
    )

    # Initialize the polynomial uncertainty term for second term
    delta_p_j_i_squared: ndarray = zeros(len(distances))
    covariance_matrix: ndarray = calculate_covariance_matrix(
        delta_shifted_intensities, distances, coefficients
    )

    # Calculate the polynomial uncertainty contributions
    for k in range(len(coefficients)):
        for l in range(len(coefficients)):  # noqa E741
            delta_p_j_i_squared = (
                delta_p_j_i_squared
                + power(distances, k) * power(distances, l) * covariance_matrix[k, l]
            )

    gaussian_error_from_polynomial_uncertainties: ndarray = (
        power(unshifted_intensities, 2)
        / power(
            calculated_differentiated_polynomial_sum_at_measuring_distances,
            4,
        )
    ) * power(delta_p_j_i_squared, 2)

    error_from_covariance: ndarray = (
        unshifted_intensities * taufactor * delta_p_j_i_squared
    ) / power(calculated_differentiated_polynomial_sum_at_measuring_distances, 3)

    test = gaussian_error_from_unshifted_intensity + gaussian_error_from_polynomial_uncertainties
    res = test + error_from_covariance
    # Return the sum of all three contributions
    return res
