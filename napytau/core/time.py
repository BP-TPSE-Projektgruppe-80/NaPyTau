import numpy as np
import scipy as sp

from napytau.import_export.model.dataset import DataSet

def calculate_times_from_distances_and_relative_velocity(
    dataset: DataSet,
) -> np.ndarray:
    return np.array(
        dataset.get_datapoints().get_distances().get_values()
        / (
            dataset.get_relative_velocity().value.get_velocity()
            * sp.constants.speed_of_light
        )
    )