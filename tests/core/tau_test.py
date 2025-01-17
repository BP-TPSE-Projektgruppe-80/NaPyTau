import unittest
from unittest.mock import MagicMock, patch
import numpy as np
from typing import Tuple


def set_up_mocks() -> (MagicMock, MagicMock):
    chi_mock = MagicMock()
    chi_mock.optimize_coefficients = MagicMock()
    chi_mock.optimize_t_hyp = MagicMock()

    polynomials_mock = MagicMock()
    polynomials_mock.differentiated_polynomial_sum_at_measuring_times = MagicMock()

    return chi_mock, polynomials_mock


class TauUnitTest(unittest.TestCase):
    def test_CanCalculateTau(self):
        """Can calculate tau"""
        chi_mock, polynomials_mock = set_up_mocks()

        # Mocked return values of called functions
        chi_mock.optimize_coefficients.return_value: Tuple[np.ndarray, float] = (
            np.array([2, 3, 1]),
            0,
        )
        chi_mock.optimize_t_hyp.return_value: float = 2.0
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

            doppler_shifted_intensities: np.ndarray = np.array([2, 6])
            unshifted_intensities: np.ndarray = np.array([6, 10])
            delta_doppler_shifted_intensities: np.ndarray = np.array([1, 1])
            delta_unshifted_intensities: np.ndarray = np.array([1, 1])
            initial_coefficients: np.ndarray = np.array([1, 1, 1])
            distances: np.ndarray = np.array([0, 1])
            t_hyp_range: (float, float) = (-5, 5)
            weight_factor: float = 1.0

            # Expected result
            expected_tau: np.ndarray = np.array([3, 1.6666667])

            np.testing.assert_array_almost_equal(
                calculate_tau_i_values(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    initial_coefficients,
                    distances,
                    t_hyp_range,
                    weight_factor,
                    None,
                ),
                expected_tau,
            )

            self.assertEqual(len(chi_mock.optimize_coefficients.mock_calls), 1)

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[0],
                (np.array([2, 6])),
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[1],
                (np.array([6, 10])),
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[2],
                (np.array([1, 1])),
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[3],
                (np.array([1, 1])),
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[4],
                (np.array([1, 1, 1])),
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[5],
                (np.array([0, 1])),
            )

            self.assertEqual(
                chi_mock.optimize_coefficients.mock_calls[0].args[6],
                2.0,
            )

            self.assertEqual(chi_mock.optimize_coefficients.mock_calls[0].args[7], 1.0)

            self.assertEqual(len(chi_mock.optimize_t_hyp.mock_calls), 1)

            np.testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[0],
                (np.array([2, 6])),
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[1],
                (np.array([6, 10])),
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[2],
                (np.array([1, 1])),
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[3],
                (np.array([1, 1])),
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[4],
                (np.array([1, 1, 1])),
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[5],
                (np.array([0, 1])),
            )

            self.assertEqual(
                chi_mock.optimize_t_hyp.mock_calls[0].args[6],
                (-5, 5),
            )

            self.assertEqual(chi_mock.optimize_t_hyp.mock_calls[0].args[7], 1.0)

            self.assertEqual(
                len(
                    polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls
                ),
                1,
            )

            np.testing.assert_array_equal(
                polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[0],
                (np.array([0, 1])),
            )

            np.testing.assert_array_equal(
                polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (np.array([2, 3, 1])),
            )
