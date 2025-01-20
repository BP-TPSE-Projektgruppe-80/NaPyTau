from napytau.core.chi import optimize_t_hyp
from napytau.core.chi import optimize_coefficients
from napytau.core.polynomials import (
    evaluate_differentiated_polynomial_at_measuring_distances,
)  # noqa E501
import numpy as np
from typing import Tuple, Optional
from napytau.import_export.model.dataset import DataSet


def calculate_tau_i_values(
    dataset: DataSet,
    initial_coefficients: np.ndarray,
    t_hyp_range: Tuple[float, float],
    weight_factor: float,
    custom_t_hyp_estimate: Optional[float],
) -> np.ndarray:
    """
    Calculates the decay times (tau_i) based on the provided
    intensities and time points.

    Args:
        dataset (DataSet): The dataset of the experiment
        initial_coefficients (ndarray):
        Initial guess for the polynomial coefficients
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
            dataset,
            initial_coefficients,
            t_hyp_range,
            weight_factor,
        )

    # optimize the polynomial coefficients with the optimized t_hyp
    optimized_coefficients: np.ndarray = (
        optimize_coefficients(
            dataset,
            initial_coefficients,
            t_hyp,
            weight_factor,
        )
    )[0]

    # calculate decay times using the optimized coefficients
    tau_i_values: np.ndarray = (
        dataset.get_datapoints().get_unshifted_intensities().get_values()
        / evaluate_differentiated_polynomial_at_measuring_distances(
            dataset, optimized_coefficients
        )
    )

    return tau_i_values
