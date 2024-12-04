from napytau.core.chi import optimize_t_hyp
from napytau.core.chi import optimize_coefficients
from napytau.core.polynomials import differentiated_polynomial_sum_at_measuring_times
from numpy import array


def calculate_tau_i(
    doppler_shifted_intensities: array,
    unshifted_intensities: array,
    delta_doppler_shifted_intensities: array,
    delta_unshifted_intensities: array,
    initial_coefficients: array,
    times: array,
    t_hyp_range: (float, float),
    weight_factor: float,
) -> array:
    """
       Calculates the decay times (tau_i) based on the provided intensities and time points.

       Args:
           doppler_shifted_intensities (array): Array of Doppler-shifted intensity measurements
           unshifted_intensities (array): Array of unshifted intensity measurements
           delta_doppler_shifted_intensities (array): Uncertainties in Doppler-shifted intensities
           delta_unshifted_intensities (array): Uncertainties in unshifted intensities
           initial_coefficients (array): Initial guess for the polynomial coefficients
           times (array): Array of time points corresponding to measurements
           t_hyp_range (tuple): Range for hypothesis optimization (min, max)
           weight_factor (float): Weighting factor for unshifted intensities

       Returns:
           array: Calculated decay times for each time point.
    """

    # optimize the hypothesis value (t_hyp) to minimize chi-squared
    t_opt: float = optimize_t_hyp(
        doppler_shifted_intensities,
        unshifted_intensities,
        delta_doppler_shifted_intensities,
        delta_unshifted_intensities,
        times,
        t_hyp_range,
        weight_factor,
        initial_coefficients,
    )

    # optimize the polynomial coefficients with the optimized t_hyp
    optimized_coefficients: array = (
        optimize_coefficients(
            doppler_shifted_intensities,
            unshifted_intensities,
            delta_doppler_shifted_intensities,
            delta_unshifted_intensities,
            times,
            t_opt,
            weight_factor,
            initial_coefficients,
        )
    )[0]

    # calculate decay times using the optimized coefficients
    tau_i: array = (
        unshifted_intensities
        / differentiated_polynomial_sum_at_measuring_times(
            times, optimized_coefficients
        )
    )

    return tau_i
