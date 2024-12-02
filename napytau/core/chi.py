from napytau.core.polynomials import polynomial_sum_at_measuring_times
from napytau.core.polynomials import differentiated_polynomial_sum_at_measuring_times
from numpy import sum
from numpy import array
from numpy import mean
from numpy import power
from scipy.optimize import minimize
from scipy.optimize import OptimizeResult


# Chi^2 Funktion für festes t-hyp
def chi_squared_fixed_t(
    doppler_shifted_intensities: array,
    unshifted_intensities: array,
    delta_doppler_shifted_intensities: array,
    delta_unshifted_intensities: array,
    coefficients: array,
    times: array,
    t_hyp: float,
    weight_factor: float,
) -> float:
    """
    Computes the chi-squared value for a given hypothesis t_hyp

    Args:
        doppler_shifted_intensities (array): Array of Doppler-shifted intensity measurements
        unshifted_intensities (array): Array of unshifted intensity measurements
        delta_doppler_shifted_intensities (array): Uncertainties in Doppler-shifted intensities
        delta_unshifted_intensities (array): Uncertainties in unshifted intensities
        coefficients (array): Polynomial coefficients for fitting
        times (array): Array of time points
        t_hyp (float): Hypothesis value for the scaling factor
        weight_factor (float): Weighting factor for unshifted intensities

    Returns:
        float: The chi-squared value for the given inputs.
    """

    # Compute the difference between Doppler-shifted intensities and polynomial model
    shifted_intensity_difference: array = (
        doppler_shifted_intensities
        - polynomial_sum_at_measuring_times(times, coefficients)
    ) / delta_doppler_shifted_intensities

    # Compute the difference between unshifted intensities and scaled derivative of the polynomial model
    unshifted_intensity_difference: array = (
        unshifted_intensities
        - (
            t_hyp
            * differentiated_polynomial_sum_at_measuring_times(times, coefficients)
        )
    ) / delta_unshifted_intensities

    # combine the weighted sum of squared differences
    return sum(
        (power(shifted_intensity_difference, 2))
        + (weight_factor * (power(unshifted_intensity_difference, 2)))
    )



def optimize_coefficients(
    doppler_shifted_intensities: array,
    unshifted_intensities: array,
    delta_doppler_shifted_intensities: array,
    delta_unshifted_intensities: array,
    initial_coefficients: array,
    times: array,
    t_hyp: float,
    weight_factor: float,
) -> (array, float):
    """
    Optimizes the polynomial coefficients to minimize the chi-squared function.

    Args:
        doppler_shifted_intensities (array): Array of Doppler-shifted intensity measurements
        unshifted_intensities (array): Array of unshifted intensity measurements
        delta_doppler_shifted_intensities (array): Uncertainties in Doppler-shifted intensities
        delta_unshifted_intensities (array): Uncertainties in unshifted intensities
        initial_coefficients (array): Initial guess for the polynomial coefficients
        times (array): Array of time points
        t_hyp (float): Hypothesis value for the scaling factor
        weight_factor (float): Weighting factor for unshifted intensities

    Returns:
        tuple: Optimized coefficients (array) and minimized chi-squared value (float).
        """
    result: array = minimize(
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
        method="L-BFGS-B", # Optimization method for bounded optimization
    )

    # Return optimized coefficients and chi-squared value
    return result.x, result.fun


def optimize_t_hyp(
    doppler_shifted_intensities: array,
    unshifted_intensities: array,
    delta_doppler_shifted_intensities: array,
    delta_unshifted_intensities: array,
    initial_coefficients: array,
    time: array,
    t_hyp_range: (float, float),
    weight_factor: float,
) -> float:
    """
    Optimizes the hypothesis value t_hyp to minimize the chi-squared function.

    Parameters:
        doppler_shifted_intensities (array): Array of Doppler-shifted intensity measurements
        unshifted_intensities (array): Array of unshifted intensity measurements
        delta_doppler_shifted_intensities (array): Uncertainties in Doppler-shifted intensities
        delta_unshifted_intensities (array): Uncertainties in unshifted intensities
        initial_coefficients (array): Initial guess for the polynomial coefficients
        time (array): Array of time points
        t_hyp_range (tuple): Range for t_hyp optimization (min, max)
        weight_factor (float): Weighting factor for unshifted intensities

    Returns:
        float: Optimized t_hyp value.
    """

    # defines a function for chi-squared computation with fixed t_hyp
    def chi_squared_t_hyp(t_hyp: float) -> float:
        # return the minimized chi-squared value for the current t_hyp
        return optimize_coefficients(
            doppler_shifted_intensities,
            unshifted_intensities,
            delta_doppler_shifted_intensities,
            delta_unshifted_intensities,
            time,
            t_hyp,
            weight_factor,
            initial_coefficients,
        )[1]

    # minimize chi-squared function over the range of t_hyp
    result: OptimizeResult = minimize(
        chi_squared_t_hyp,
        x0=mean(t_hyp_range), # Initial guess for t_hyp
        bounds=[(t_hyp_range[0], t_hyp_range[1])], # Boundaries for optimization
    )

    # Return optimized t_hyp value
    return result.x
