from napytau.core.chi import optimize_t_hyp
from napytau.core.chi import optimize_coefficients
from napytau.core.polynomials import differentiated_polynomial_sum_at_measuring_times
from numpy import array


def calculate_tau_i(doppler_shifted_intensities: array,
                    unshifted_intensities: array,
                    delta_doppler_shifted_intensities: array,
                    delta_unshifted_intensities: array,
                    initial_coefficients: array,
                    times: array,
                    t_hyp_range: (float, float),
                    weight_factor: float) -> array:
    t_opt: float = optimize_t_hyp(doppler_shifted_intensities,
                                  unshifted_intensities,
                                  delta_doppler_shifted_intensities,
                                  delta_unshifted_intensities,
                                  times,
                                  t_hyp_range,
                                  weight_factor,
                                  initial_coefficients)

    optimized_coefficients: array= (
        optimize_coefficients(doppler_shifted_intensities,
                              unshifted_intensities,
                              delta_doppler_shifted_intensities,
                              delta_unshifted_intensities,
                              times,
                              t_opt,
                              weight_factor,
                              initial_coefficients))[0]

    tau_i: array = (doppler_shifted_intensities
                    / differentiated_polynomial_sum_at_measuring_times(
                                                        times, optimized_coefficients))

    return tau_i
