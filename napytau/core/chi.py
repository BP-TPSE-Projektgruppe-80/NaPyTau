from napytau.core.polynomials import polynomial_sum_at_measuring_times
from napytau.core.polynomials import differentiated_polynomial_sum_at_measuring_times
from numpy import sum
from numpy import ndarray
from numpy import mean
from numpy import power
from scipy.optimize import minimize
from scipy.optimize import OptimizeResult
from typing import Tuple


# Chi^2 Funktion für festes t-hyp
def chi_squared_fixed_t(
    doppler_shifted_intensities: ndarray,
    unshifted_intensities: ndarray,
    delta_doppler_shifted_intensities: ndarray,
    delta_unshifted_intensities: ndarray,
    coefficients: ndarray,
    times: ndarray,
    t_hyp: float,
    weight_factor: float,
) -> float:
    """
    Computes the chi-squared value for a given hypothesis t_hyp

    Args:
        doppler_shifted_intensities (ndarray):
        Array of Doppler-shifted intensity measurements
        unshifted_intensities (ndarray):
        Array of unshifted intensity measurements
        delta_doppler_shifted_intensities (ndarray):
        Uncertainties in Doppler-shifted intensities
        delta_unshifted_intensities (ndarray):
        Uncertainties in unshifted intensities
        coefficients (ndarray):
        Polynomial coefficients for fitting
        times (ndarray):
        Array of time points
        t_hyp (float):
        Hypothesis value for the scaling factor
        weight_factor (float):
        Weighting factor for unshifted intensities

    Returns:
        float: The chi-squared value for the given inputs.
    """

    # Compute the difference between Doppler-shifted intensities and polynomial model
    shifted_intensity_difference: ndarray = (
        doppler_shifted_intensities
        - polynomial_sum_at_measuring_times(times, coefficients)
    ) / delta_doppler_shifted_intensities

    # Compute the difference between unshifted intensities and
    # scaled derivative of the polynomial model
    unshifted_intensity_difference: ndarray = (
        unshifted_intensities
        - (
            t_hyp
            * differentiated_polynomial_sum_at_measuring_times(times, coefficients)
        )
    ) / delta_unshifted_intensities

    # combine the weighted sum of squared differences
    result: float = sum(
        (power(shifted_intensity_difference, 2))
        + (weight_factor * (power(unshifted_intensity_difference, 2)))
    )
    return result

def optimize_coefficients(
    doppler_shifted_intensities: ndarray,
    unshifted_intensities: ndarray,
    delta_doppler_shifted_intensities: ndarray,
    delta_unshifted_intensities: ndarray,
    initial_coefficients: ndarray,
    times: ndarray,
    t_hyp: float,
    weight_factor: float,
) -> Tuple[ndarray, float]:
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
        times (ndarray):
        Array of time points
        t_hyp (float):
        Hypothesis value for the scaling factor
        weight_factor (float):
        Weighting factor for unshifted intensities

    Returns:
        tuple: Optimized coefficients (ndarray) and minimized chi-squared value (float).
    """
    result: OptimizeResult = minimize(
        lambda coefficients: chi_squared_fixed_t(
            doppler_shifted_intensities,
            unshifted_intensities,
            delta_doppler_shifted_intensities,
            delta_unshifted_intensities,
            coefficients,
            times,
            t_hyp,
            weight_factor,
        ),
        initial_coefficients,
        method="L-BFGS-B",  # Optimization method for bounded optimization
    )

    # Return optimized coefficients and chi-squared value
    return result.x, result.fun


def optimize_t_hyp(
    doppler_shifted_intensities: ndarray,
    unshifted_intensities: ndarray,
    delta_doppler_shifted_intensities: ndarray,
    delta_unshifted_intensities: ndarray,
    initial_coefficients: ndarray,
    time: ndarray,
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
        time (ndarray):
        Array of time points
        t_hyp_range (tuple):
        Range for t_hyp optimization (min, max)
        weight_factor (float):
        Weighting factor for unshifted intensities

    Returns:
        float: Optimized t_hyp value.
    """

    # defines a function for chi-squared computation with fixed t_hyp
    # return the minimized chi-squared value for the current t_hyp
    chi_squared_t_hyp = lambda t_hyp: optimize_coefficients(
        doppler_shifted_intensities,
        unshifted_intensities,
        delta_doppler_shifted_intensities,
        delta_unshifted_intensities,
        time,
        initial_coefficients,
        t_hyp,
        weight_factor,
    )[1]

    # minimize chi-squared function over the range of t_hyp
    result: OptimizeResult = minimize(
        chi_squared_t_hyp,
        x0=mean(t_hyp_range),  # Initial guess for t_hyp
        bounds=[(t_hyp_range[0], t_hyp_range[1])],  # Boundaries for optimization
    )

    # Return optimized t_hyp value
    optimized_t_hyp: float = result.x
    return optimized_t_hyp
