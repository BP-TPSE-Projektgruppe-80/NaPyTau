from napytau.core.chi import optimize_t_hyp
from napytau.core.chi import optimize_coefficients
from napytau.core.polynomials import differentiated_polynomial_sum_at_measuring_times
from numpy import ndarray
from typing import Tuple


def calculate_tau_i(
    doppler_shifted_intensities: ndarray,
    unshifted_intensities: ndarray,
    delta_doppler_shifted_intensities: ndarray,
    delta_unshifted_intensities: ndarray,
    initial_coefficients: ndarray,
    times: ndarray,
    t_hyp_range: Tuple[float, float],
    weight_factor: float,
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
           times (ndarray):
           Array of time points corresponding to measurements
           t_hyp_range (tuple):
           Range for hypothesis optimization (min, max)
           weight_factor (float):
           Weighting factor for unshifted intensities

       Returns:
           ndarray: Calculated decay times for each time point.
    """

    # optimize the hypothesis value (t_hyp) to minimize chi-squared
    t_opt: float = optimize_t_hyp(
        doppler_shifted_intensities,
        unshifted_intensities,
        delta_doppler_shifted_intensities,
        delta_unshifted_intensities,
        initial_coefficients,
        times,
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
            times,
            t_opt,
            weight_factor,
        )
    )[0]

    # calculate decay times using the optimized coefficients
    tau_i: ndarray = (
        unshifted_intensities
        / differentiated_polynomial_sum_at_measuring_times(
            times, optimized_coefficients
        )
    )

    return tau_i
