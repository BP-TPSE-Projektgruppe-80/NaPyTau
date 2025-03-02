import unittest
from random import random
from unittest.mock import MagicMock, patch
import numpy as np
from typing import Tuple
from napytau.import_export.model.datapoint_collection import DatapointCollection
from napytau.import_export.model.dataset import DataSet
from napytau.import_export.model.relative_velocity import RelativeVelocity
from napytau.util.model.value_error_pair import ValueErrorPair
from napytau.import_export.model.datapoint import Datapoint


def set_up_mocks() -> (MagicMock, MagicMock):
    chi_mock = MagicMock()
    chi_mock.optimize_coefficients = MagicMock()
    chi_mock.optimize_t_hyp = MagicMock()

    polynomials_mock = MagicMock()
    polynomials_mock.differentiated_polynomial_sum_at_measuring_times = MagicMock()

    return chi_mock, polynomials_mock


def _get_dataset_stub(datapoints: DatapointCollection) -> DataSet:
    return DataSet(
        ValueErrorPair(RelativeVelocity(random()), RelativeVelocity(random())),
        datapoints,
    )


class TauUnitTest(unittest.TestCase):
    def test_CanCalculateTau(self):
        """Can calculate tau"""
        chi_mock, polynomials_mock = set_up_mocks()

        # Mocked return values of called functions
        chi_mock.optimize_coefficients.return_value: Tuple[np.ndarray, float] = (
            np.array([2, 3, 1]),
            0,
        )
        chi_mock.optimize_tau_factor.return_value: float = 2.0
        polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.return_value: np.ndarray = np.array(
            [2, 6]
        )

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.polynomials": polynomials_mock,
                "napytau.core.chi": chi_mock,
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
            t_hyp_range: (float, float) = (-5, 5)
            weight_factor: float = 1.0

            # Expected result
            expected_tau: np.ndarray = np.array([3, 1.6666667])

            np.testing.assert_array_almost_equal(
                calculate_tau_i_values(
                    dataset,
                    initial_coefficients,
                    t_hyp_range,
                    weight_factor,
                    None,
                ),
                expected_tau,
            )

            self.assertEqual(len(chi_mock.optimize_coefficients.mock_calls), 1)

            self.assertEqual(
                chi_mock.optimize_coefficients.mock_calls[0].args[0],
                dataset,
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[1],
                (np.array([1, 1, 1])),
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[2],
                2.0,
            )

            self.assertEqual(
                chi_mock.optimize_coefficients.mock_calls[0].args[3],
                1.0,
            )

            self.assertEqual(len(chi_mock.optimize_tau_factor.mock_calls), 1)

            self.assertEqual(
                chi_mock.optimize_coefficients.mock_calls[0].args[0],
                dataset,
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_tau_factor.mock_calls[0].args[1],
                (np.array([1, 1, 1])),
            )

            self.assertEqual(
                chi_mock.optimize_tau_factor.mock_calls[0].args[2],
                (-5, 5),
            )

            self.assertEqual(chi_mock.optimize_tau_factor.mock_calls[0].args[3], 1.0)

            self.assertEqual(
                len(
                    polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls
                ),
                1,
            )

            self.assertEqual(
                polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[0],
                dataset,
            )

            np.testing.assert_array_equal(
                polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (np.array([2, 3, 1])),
            )
