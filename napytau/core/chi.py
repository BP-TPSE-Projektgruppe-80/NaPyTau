from napytau.core.polynomials import polynomial_sum_at_measuring_times
from napytau.core.polynomials import differentiated_polynomial_sum_at_measuring_times
from numpy import sum
from numpy import array
from numpy import mean
from numpy import power
from scipy.optimize import minimize
from scipy.optimize import OptimizeResult


# Chi^2 Funktion für festes t-hyp
def chi_squared_fixed_t(doppler_shifted_intensities: array,
                        unshifted_intensities: array,
                        delta_doppler_shifted_intensities: array,
                        delta_unshifted_intensities: array,
                        coefficients: array,
                        times: array,
                        t_hyp: float,
                        weight_factor: float) -> float:

    shifted_intensity_difference: array = (
            (doppler_shifted_intensities
             - polynomial_sum_at_measuring_times(times, coefficients))
            / delta_doppler_shifted_intensities)
    unshifted_intensity_difference: array = (
            (unshifted_intensities
             - (t_hyp
             * differentiated_polynomial_sum_at_measuring_times(times, coefficients)))
            / delta_unshifted_intensities)
    return sum((power(shifted_intensity_difference, 2))
               + (weight_factor * (power(unshifted_intensity_difference, 2))))


#Minimierung von chi^2 über t-hyp
def optimize_coefficients(doppler_shifted_intensities: array,
                          unshifted_intensities: array,
                          delta_doppler_shifted_intensities: array,
                          delta_unshifted_intensities: array,
                          initial_coefficients: array,
                          times: array,
                          t_hyp: float,
                          weight_factor: float) -> (array, float):
    result: array = minimize(lambda coefficients:
                             chi_squared_fixed_t(doppler_shifted_intensities,
                                                 unshifted_intensities,
                                                 delta_doppler_shifted_intensities,
                                                 delta_unshifted_intensities,
                                                 coefficients,
                                                 times,
                                                 t_hyp,
                                                 weight_factor),
                             initial_coefficients,
                             method='L-BFGS-B')
    return result.x, result.fun


def optimize_t_hyp(doppler_shifted_intensities: array,
                   unshifted_intensities: array,
                   delta_doppler_shifted_intensities: array,
                   delta_unshifted_intensities: array,
                   initial_coefficients: array,
                   time: array,
                   t_hyp_range: (float, float),
                   weight_factor: float) -> float:
    def chi_squared_t_hyp(t_hyp: float) -> float:
        chi_squared: float = optimize_coefficients(doppler_shifted_intensities,
                                                   unshifted_intensities,
                                                   delta_doppler_shifted_intensities,
                                                   delta_unshifted_intensities,
                                                   time,
                                                   t_hyp,
                                                   weight_factor,
                                                   initial_coefficients)[1]
        return chi_squared

    result: OptimizeResult = minimize(chi_squared_t_hyp,
                                      x0 = mean(t_hyp_range),
                                      bounds = [(t_hyp_range[0],
                                      t_hyp_range[1])])
    return result.x
