from napytau.core.polynomials import (
    evaluate_differentiated_polynomial_at_measuring_distances,
)
from napytau.core.polynomials import evaluate_polynomial_at_measuring_distances
import numpy as np

from napytau.import_export.model.dataset import DataSet


def calculate_jacobian_matrix(
    dataset: DataSet,
    coefficients: np.ndarray,
) -> np.ndarray:
    """
    calculated the jacobian matrix for a set of polynomial coefficients taking
    different distances into account.
    Adds Disturbances to each coefficient to calculate partial derivatives,
    safes them in jacobian matrix
    Args:
        dataset (DataSet): The dataset of the experiment
        Datapoints for fitting, consisting of distances and intensities
        coefficients (ndarray): Array of polynomial coefficients.

    Returns:
        ndarray:
        The computed Jacobian matrix with shape (len(distances), len(coefficients)).
    """

    datapoints = dataset.get_datapoints()
    # initializes the jacobian matrix
    jacobian_matrix: np.ndarray = np.zeros(
        (len(datapoints.get_distances().get_values()), len(coefficients))
    )

    epsilon: float = 1e-6  # small disturbance value

    # Loop over each coefficient and calculate the partial derivative
    for i in range(len(coefficients)):
        perturbed_coefficients: np.ndarray = np.array(coefficients, dtype=float)
        perturbed_coefficients[i] += epsilon  # slightly disturb the current coefficient

        # Compute the disturbed and original polynomial values at the given distances
        perturbed_function: np.ndarray = evaluate_polynomial_at_measuring_distances(
            dataset, perturbed_coefficients
        )
        original_function: np.ndarray = evaluate_polynomial_at_measuring_distances(
            dataset, coefficients
        )

        # Calculate the partial derivative coefficients and store it in the
        # Jacobian matrix
        # jacobian_matrix[:, i] selects the entire column i of the jacobian matrix
        # The colon (:) indicates all rows and i specifies the column
        jacobian_matrix[:, i] = (perturbed_function - original_function) / epsilon

    return jacobian_matrix


def calculate_covariance_matrix(
    dataset: DataSet,
    coefficients: np.ndarray,
) -> np.ndarray:
    """
    Computes the covariance matrix for the polynomial coefficients using the
    jacobian matrix and a weight matrix derived from the shifted intensities' errors.
    Args:
        dataset (Dataset): The dataset of the experiment
        Datapoints for fitting, consisting of distances and intensities
        coefficients (ndarray): Array of polynomial coefficients.

    Returns:
        ndarray: The computed covariance matrix for the polynomial coefficients.
    """

    datapoints = dataset.get_datapoints()
    jacobian_matrix: np.ndarray = calculate_jacobian_matrix(dataset, coefficients)

    # Construct the weight matrix from the inverse squared errors
    weight_matrix: np.ndarray = np.diag(
        1 / np.power(datapoints.get_shifted_intensities().get_errors(), 2)
    )

    fit_matrix: np.ndarray = jacobian_matrix.T @ weight_matrix @ jacobian_matrix

    covariance_matrix: np.ndarray = np.linalg.inv(fit_matrix)

    return covariance_matrix


def calculate_error_propagation_terms(
    dataset: DataSet,
    coefficients: np.ndarray,
    taufactor: float,
) -> np.ndarray:
    """
    creates the error propagation term for the polynomial coefficients.
    combining direct errors, polynomial uncertainties, and mixed covariance terms.
    Args:
        dataset (DataSet): The dataset of the experiment
        coefficients (ndarray): Array of polynomial coefficients.
        taufactor (float): Scaling factor related to the Doppler-shift model.

    Returns:
        ndarray: The combined error propagation terms for each distance point.
    """

    datapoints = dataset.get_datapoints()
    calculated_differentiated_polynomial_sum_at_measuring_distances = (
        evaluate_differentiated_polynomial_at_measuring_distances(  # noqa E501
            dataset,
            coefficients,
        )
    )

    gaussian_error_from_unshifted_intensity: np.ndarray = np.power(
        datapoints.get_unshifted_intensities().get_errors(), 2
    ) / np.power(
        calculated_differentiated_polynomial_sum_at_measuring_distances,
        2,
    )

    # Initialize the polynomial uncertainty term for second term
    delta_p_j_i_squared: np.ndarray = np.zeros(
        len(datapoints.get_distances().get_values())
    )
    covariance_matrix: np.ndarray = calculate_covariance_matrix(dataset, coefficients)

    # Calculate the polynomial uncertainty contributions
    for k in range(len(coefficients)):
        for l in range(len(coefficients)):  # noqa E741
            delta_p_j_i_squared = (
                delta_p_j_i_squared
                + np.power(datapoints.get_distances().get_values(), k)
                * np.power(datapoints.get_distances().get_values(), l)
                * covariance_matrix[k, l]
            )

    gaussian_error_from_polynomial_uncertainties: np.ndarray = (
        np.power(datapoints.get_unshifted_intensities().get_values(), 2)
        / np.power(
            calculated_differentiated_polynomial_sum_at_measuring_distances,
            4,
        )
    ) * np.power(delta_p_j_i_squared, 2)

    error_from_covariance: np.ndarray = (
        datapoints.get_unshifted_intensities().get_values()
        * taufactor
        * delta_p_j_i_squared
    ) / np.power(calculated_differentiated_polynomial_sum_at_measuring_distances, 3)

    interim_result: np.ndarray = (
        gaussian_error_from_unshifted_intensity
        + gaussian_error_from_polynomial_uncertainties
    )
    errors: np.ndarray = interim_result + error_from_covariance
    # Return the sum of all three contributions
    return errors
