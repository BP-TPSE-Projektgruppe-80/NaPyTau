from napytau.util.model.value_error_pair import ValueErrorPair
import numpy as np
from typing import List


def get_values_from_value_error_pair_list(value_error_pair_list: List[ValueErrorPair[float]]) -> np.ndarray:
    values: np.ndarray = np.ndarray(shape=len(value_error_pair_list), dtype=float)

    for i in range(len(value_error_pair_list)):
        values[i] = value_error_pair_list[i].value

    return values


def get_errors_from_value_error_pair_list(value_error_pair_list: List[ValueErrorPair[float]]) -> np.ndarray:
    errors: np.ndarray = np.zeros(shape=len(value_error_pair_list), dtype=float)

    for i in range(len(value_error_pair_list)):
        errors[i] = value_error_pair_list[i].error

    return errors