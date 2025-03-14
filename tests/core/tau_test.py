import unittest
from random import random
from unittest.mock import MagicMock, patch
import numpy as np
from napytau.import_export.model.datapoint_collection import DatapointCollection
from napytau.import_export.model.dataset import DataSet
from napytau.import_export.model.relative_velocity import RelativeVelocity
from napytau.util.model.value_error_pair import ValueErrorPair
from napytau.import_export.model.datapoint import Datapoint


def set_up_mocks() -> MagicMock:
    polynomials_mock = MagicMock()
    polynomials_mock.differentiated_polynomial_sum_at_measuring_times = MagicMock()

    return polynomials_mock

def _get_dataset_stub(datapoints: DatapointCollection) -> DataSet:
    return DataSet(
        ValueErrorPair(RelativeVelocity(random()), RelativeVelocity(random())),
        datapoints,
    )


def _get_dataset_stub(datapoints: DatapointCollection) -> DataSet:
    return DataSet(
        ValueErrorPair(RelativeVelocity(random()), RelativeVelocity(random())),
        datapoints,
    )


class TauUnitTest(unittest.TestCase):
    def test_CanCalculateTau(self):
        """Can calculate tau"""
        polynomials_mock = set_up_mocks()

        polynomials_mock.evaluate_differentiated_polynomial_at_measuring_times.return_value: np.ndarray = np.array(
            [2, 6]
        )

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.polynomials": polynomials_mock,
            },
        ):
            from napytau.core.tau import calculate_tau_i_values

            initial_coefficients: np.ndarray = np.array([1, 1, 1])
            datapoints = DatapointCollection(
                [
                    Datapoint(
                        ValueErrorPair(0.0, 0.16),
                        None,
                        ValueErrorPair(2, 1),
                        ValueErrorPair(6, 1),
                    ),
                    Datapoint(
                        ValueErrorPair(1.0, 0.16),
                        None,
                        ValueErrorPair(6, 1),
                        ValueErrorPair(10, 1),
                    ),
                ]
            )
            dataset = _get_dataset_stub(datapoints)

            # Expected result
            expected_tau: np.ndarray = np.array([3, 1.6666667])

            np.testing.assert_array_almost_equal(
                calculate_tau_i_values(
                    dataset,
                    initial_coefficients,
                ),
                expected_tau,
            )

            self.assertEqual(
                len(
                    polynomials_mock.evaluate_differentiated_polynomial_at_measuring_times.mock_calls
                ),
                1,
            )

            self.assertEqual(
                polynomials_mock.evaluate_differentiated_polynomial_at_measuring_times.mock_calls[
                    0
                ].args[0],
                dataset,
            )

            np.testing.assert_array_equal(
                polynomials_mock.evaluate_differentiated_polynomial_at_measuring_times.mock_calls[
                    0
                ].args[1],
                (np.array([1, 1, 1])),
            )
