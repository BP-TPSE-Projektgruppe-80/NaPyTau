from napytau.core.chi import optimize_t_hyp
from napytau.core.chi import optimize_coefficients
from napytau.core.polynomials import (
    evaluate_differentiated_polynomial_at_measuring_distances,
)  # noqa E501
from numpy import ndarray
from typing import Tuple, Optional


def calculate_tau_i_values(
    doppler_shifted_intensities: ndarray,
    unshifted_intensities: ndarray,
    delta_doppler_shifted_intensities: ndarray,
    delta_unshifted_intensities: ndarray,
    initial_coefficients: ndarray,
    distances: ndarray,
    relative_velocity: float,
    t_hyp_range: Tuple[float, float],
    weight_factor: float,
    custom_t_hyp_estimate: Optional[float],
) -> ndarray:
    """
    Calculates the decay times (tau_i) based on the provided
    intensities and time points.

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
        Array of distance points corresponding to measurements
        relative_velocity (float):
        Velocity, relative to the speed of light
        t_hyp_range (tuple):
        Range for hypothesis optimization (min, max)
        weight_factor (float):
        Weighting factor for unshifted intensities

    Returns:
        ndarray: Calculated decay times for each distance point.
    """

    # If a custom hypothesis for t_hyp is given, we use it for the further calculations
    # Otherwise we optimize the hypothesis value (t_hyp) to minimize chi-squared
    if custom_t_hyp_estimate is not None:
        t_hyp: float = custom_t_hyp_estimate
    else:
        t_hyp = optimize_t_hyp(
            doppler_shifted_intensities,
            unshifted_intensities,
            delta_doppler_shifted_intensities,
            delta_unshifted_intensities,
            initial_coefficients,
            distances,
            relative_velocity,
            t_hyp_range,
            weight_factor,
        )

    # optimize the polynomial coefficients with the optimized t_hyp
    optimized_coefficients: ndarray = (
        optimize_coefficients(
            doppler_shifted_intensities,
            unshifted_intensities,
            delta_doppler_shifted_intensities,
            delta_unshifted_intensities,
            initial_coefficients,
            distances,
            relative_velocity,
            t_hyp,
            weight_factor,
        )
    )[0]

    # calculate decay times using the optimized coefficients
    tau_i_values: ndarray = (
        unshifted_intensities
        / evaluate_differentiated_polynomial_at_measuring_distances(
            distances, relative_velocity, optimized_coefficients
        )
    )

    return tau_i_values
