import numpy as np
from napytau.core.chi import optimize_t_hyp
from napytau.core.chi import optimize_coefficients
from napytau.core.tau import calculate_tau_i_values
from napytau.core.delta_tau import calculate_error_propagation_terms
from napytau.core.tau_final import calculate_tau_final
from typing import Tuple, Optional


def calculate_lifetime(doppler_shifted_intensities: np.ndarray,
                       unshifted_intensities: np.ndarray,
                       delta_doppler_shifted_intensities: np.ndarray,
                       delta_unshifted_intensities: np.ndarray,
                       initial_coefficients: np.ndarray,
                       distances: np.ndarray,
                       t_hyp_range: Tuple[float, float],
                       weight_factor: float,
                       custom_t_hyp_estimate: Optional[float]) -> Tuple[float, float]:

    # If a custom t_hyp is given, we will use it for the further calculations
    # If no custom t_hyp is given, we will use the optimal taufactor instead
    if custom_t_hyp_estimate is not None:
        t_hyp: float = custom_t_hyp_estimate
    else:
        t_hyp: float = optimize_t_hyp(doppler_shifted_intensities,
                                      unshifted_intensities,
                                      delta_doppler_shifted_intensities,
                                      delta_unshifted_intensities,
                                      initial_coefficients,
                                      distances,
                                      t_hyp_range,
                                      weight_factor)

    # Now we find the optimal coefficients for the given taufactor
    optimized_coefficients: np.ndarray = (
        optimize_coefficients(
            doppler_shifted_intensities,
            unshifted_intensities,
            delta_doppler_shifted_intensities,
            delta_unshifted_intensities,
            initial_coefficients,
            distances,
            t_hyp,
            weight_factor,
        )
    )[0]

    # We now calculate the lifetimes tau_i for all measured distances
    tau_i_values: np.ndarray = calculate_tau_i_values(doppler_shifted_intensities,
                                                      unshifted_intensities,
                                                      delta_doppler_shifted_intensities,
                                                      delta_unshifted_intensities,
                                                      initial_coefficients,
                                                      distances,
                                                      t_hyp_range,
                                                      weight_factor,
                                                      custom_t_hyp_estimate)

    # And we calculate the respective errors for the lifetimes
    delta_tau_i_values: np.ndarray = calculate_error_propagation_terms(
        unshifted_intensities,
        delta_doppler_shifted_intensities,
        delta_unshifted_intensities,
        distances,
        optimized_coefficients,
        t_hyp)

    # From lifetimes and associated errors we can now calculate the weighted mean
    # and the uncertainty
    tau_final: (float, float) = calculate_tau_final(tau_i_values, delta_tau_i_values)

    return tau_final