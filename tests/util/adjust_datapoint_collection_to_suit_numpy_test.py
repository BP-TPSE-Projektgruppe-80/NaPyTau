import unittest
from napytau.util.adjust_datapoint_collection_to_suit_numpy import (
    get_values_from_value_error_pair_list,
    get_errors_from_value_error_pair_list,
)
from napytau.util.model.value_error_pair import ValueErrorPair
from typing import List
import numpy as np


class AdjustDataPointCollectionToSuitNumPyUnitTest(unittest.TestCase):
    @staticmethod
    def test_canReturnValuesFromValidValueErrorPairList():
        """Can return values from valid ValueErrorPair list."""
        value_error_pair_list: List[ValueErrorPair] = [
            ValueErrorPair(1, 2),
            ValueErrorPair(3, 4),
            ValueErrorPair(5, 6),
        ]

        expected_values_result: np.ndarray = np.array([1, 3, 5])

        np.testing.assert_array_equal(
            get_values_from_value_error_pair_list(value_error_pair_list),
            expected_values_result,
        )

    @staticmethod
    def test_returnsEmptyValuesArrayForEmptyValueErrorPairList():
        """Returns empty values array for empty ValueErrorPair list."""
        value_error_pair_list: List[ValueErrorPair] = []

        expected_values_result: np.ndarray = np.array([])

        np.testing.assert_array_equal(
            get_values_from_value_error_pair_list(value_error_pair_list),
            expected_values_result,
        )

    @staticmethod
    def test_canReturnErrorsFromValidValueErrorPairList():
        """Can return errors from valid ValueErrorPair list."""
        value_error_pair_list: List[ValueErrorPair] = [
            ValueErrorPair(1, 2),
            ValueErrorPair(3, 4),
            ValueErrorPair(5, 6),
        ]

        expected_errors_result: np.ndarray = np.array([2, 4, 6])

        np.testing.assert_array_equal(
            get_errors_from_value_error_pair_list(value_error_pair_list),
            expected_errors_result,
        )

    @staticmethod
    def test_returnsEmptyErrorsArrayForEmptyValueErrorPairList():
        """Returns empty errors array for empty ValueErrorPair list."""
        value_error_pair_list: List[ValueErrorPair] = []

        expected_errors_result: np.ndarray = np.array([])

        np.testing.assert_array_equal(
            get_errors_from_value_error_pair_list(value_error_pair_list),
            expected_errors_result,
        )
