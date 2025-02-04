from napytau.core.chi import optimize_t_hyp
from napytau.core.chi import optimize_coefficients
from napytau.core.tau import calculate_tau_i_values
from napytau.core.delta_tau import calculate_error_propagation_terms
from napytau.core.tau_final import calculate_tau_final
from typing import Tuple, Optional
import numpy as np
from napytau.import_export.model.dataset import DataSet


def calculate_lifetime(
    dataSet: DataSet,
    initial_coefficients: np.ndarray,
    t_hyp_range: Tuple[float, float],
    weight_factor: float,
    custom_t_hyp_estimate: Optional[float],
) -> Tuple[float, float]:
    """
    Docstring missing. To be implemented with issue #44.
    """

    # If a custom t_hyp is given, we will use it for the further calculations
    # If no custom t_hyp is given, we will use the optimal taufactor instead
    if custom_t_hyp_estimate is not None:
        t_hyp = custom_t_hyp_estimate
    else:
        t_hyp = optimize_t_hyp(
            dataSet,
            initial_coefficients,
            t_hyp_range,
            weight_factor,
        )

    # Now we find the optimal coefficients for the given taufactor
    optimized_coefficients: np.ndarray = (
        optimize_coefficients(
            dataSet,
            initial_coefficients,
            t_hyp,
            weight_factor,
        )
    )[0]

    # We now calculate the lifetimes tau_i for all measured distances
    tau_i_values: np.ndarray = calculate_tau_i_values(
        dataSet,
        initial_coefficients,
        t_hyp_range,
        weight_factor,
        custom_t_hyp_estimate,
    )

    # And we calculate the respective errors for the lifetimes
    delta_tau_i_values: np.ndarray = calculate_error_propagation_terms(
        dataSet,
        optimized_coefficients,
        t_hyp,
    )

    # From lifetimes and associated errors we can now calculate the weighted mean
    # and the uncertainty
    tau_final: Tuple[float, float] = calculate_tau_final(
        tau_i_values, delta_tau_i_values
    )

    return tau_final
