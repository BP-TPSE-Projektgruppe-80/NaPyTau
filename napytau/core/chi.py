from napytau.core.polynomials import evaluate_polynomial_at_measuring_distances
from napytau.core.polynomials import (
    evaluate_differentiated_polynomial_at_measuring_distances,
)
from napytau.import_export.model.datapoint_collection import DatapointCollection
import numpy as np
import scipy as sp
from typing import Tuple


def chi_squared_fixed_t(
    datapoints: DatapointCollection,
    coefficients: np.ndarray,
    t_hyp: float,
    weight_factor: float,
) -> float:
    """
    Computes the chi-squared value for a given hypothesis t_hyp

    Args:
        datapoints (DatapointCollection):
        Datapoints for fitting, consisting of distances and intensities
        coefficients (ndarray):
        Polynomial coefficients for fitting
        t_hyp (float):
        Hypothesis value for the scaling factor
        weight_factor (float):
        Weighting factor for unshifted intensities

    Returns:
        float: The chi-squared value for the given inputs.
    """

    # Compute the difference between Doppler-shifted intensities and polynomial model
    shifted_intensity_difference: np.ndarray = (
        datapoints.get_shifted_intensities().get_values()
        - evaluate_polynomial_at_measuring_distances(datapoints.get_distances().get_values(), coefficients)
    ) / datapoints.get_shifted_intensities().get_errors()

    # Compute the difference between unshifted intensities and
    # scaled derivative of the polynomial model
    unshifted_intensity_difference: np.ndarray = (
        datapoints.get_unshifted_intensities().get_values()
        - (
            t_hyp
            * evaluate_differentiated_polynomial_at_measuring_distances(
                datapoints.get_distances().get_values(), coefficients
            )
        )
    ) / datapoints.get_unshifted_intensities().get_errors()

    # combine the weighted sum of squared differences
    result: float = np.sum(
        (np.power(shifted_intensity_difference, 2))
        + (weight_factor * (np.power(unshifted_intensity_difference, 2)))
    )

    return result


def optimize_coefficients(
    doppler_shifted_intensities: np.ndarray,
    unshifted_intensities: np.ndarray,
    delta_doppler_shifted_intensities: np.ndarray,
    delta_unshifted_intensities: np.ndarray,
    initial_coefficients: np.ndarray,
    distances: np.ndarray,
    t_hyp: float,
    weight_factor: float,
) -> Tuple[np.ndarray, float]:
    """
    Optimizes the polynomial coefficients to minimize the chi-squared function.

    Args:
        doppler_shifted_intensities (ndarray):
        Array of Doppler-shifted intensity measurements
        unshifted_intensities (ndarray):
        Array of unshifted intensity measurements
        delta_doppler_shifted_intensities (ndarray):
        Uncertainties in Doppler-shifted intensities
        delta_unshifted_intensities (ndarray):
        Uncertainties in unshifted intensities
        initial_coefficients (ndarray):
        Initial guess for the polynomial coefficients
        distances (ndarray):
        Array of distance points
        t_hyp (float):
        Hypothesis value for the scaling factor
        weight_factor (float):
        Weighting factor for unshifted intensities

    Returns:
        tuple: Optimized coefficients (ndarray) and minimized chi-squared value (float).
    """
    chi_squared = lambda coefficients: chi_squared_fixed_t(
        doppler_shifted_intensities,
        unshifted_intensities,
        delta_doppler_shifted_intensities,
        delta_unshifted_intensities,
        coefficients,
        distances,
        t_hyp,
        weight_factor,
    )

    result: sp.optimize.OptimizeResult = sp.optimize.minimize(
        chi_squared,
        initial_coefficients,
        # Optimization method for bounded optimization. It minimizes a scalar function
        # of one or more variables using the BFGS optimization algorithm,
        # which uses a limited amount of computer memory.
        method="L-BFGS-B",
    )

    # Return optimized coefficients and chi-squared value
    return result.x, result.fun


def optimize_t_hyp(
    doppler_shifted_intensities: np.ndarray,
    unshifted_intensities: np.ndarray,
    delta_doppler_shifted_intensities: np.ndarray,
    delta_unshifted_intensities: np.ndarray,
    initial_coefficients: np.ndarray,
    distances: np.ndarray,
    t_hyp_range: Tuple[float, float],
    weight_factor: float,
) -> float:
    """
    Optimizes the hypothesis value t_hyp to minimize the chi-squared function.

    Parameters:
        doppler_shifted_intensities (ndarray):
        Array of Doppler-shifted intensity measurements
        unshifted_intensities (ndarray):
        Array of unshifted intensity measurements
        delta_doppler_shifted_intensities (ndarray):
        Uncertainties in Doppler-shifted intensities
        delta_unshifted_intensities (ndarray):
        Uncertainties in unshifted intensities
        initial_coefficients (ndarray):
        Initial guess for the polynomial coefficients
        distances (ndarray):
        Array of distance points
        t_hyp_range (tuple):
        Range for t_hyp optimization (min, max)
        weight_factor (float):
        Weighting factor for unshifted intensities

    Returns:
        float: Optimized t_hyp value.
    """

    chi_squared_t_hyp = lambda t_hyp: optimize_coefficients(
        doppler_shifted_intensities,
        unshifted_intensities,
        delta_doppler_shifted_intensities,
        delta_unshifted_intensities,
        distances,
        initial_coefficients,
        t_hyp,
        weight_factor,
    )[1]

    result: sp.optimize.OptimizeResult = sp.optimize.minimize(
        chi_squared_t_hyp,
        # Initial guess for t_hyp. Startíng with the mean reduces likelihood of
        # biasing the optimization process toward one boundary.
        x0=np.mean(t_hyp_range),
        bounds=[(t_hyp_range[0], t_hyp_range[1])],
    )

    # Return optimized t_hyp value
    return float(result.x)
