import unittest
from unittest.mock import MagicMock, patch
import numpy as np
from typing import Tuple, Optional


def set_up_mocks() -> (MagicMock, MagicMock, MagicMock, MagicMock):
    chi_mock = MagicMock()
    chi_mock.optimize_t_hyp = MagicMock()
    chi_mock.optimize_coefficients = MagicMock()

    tau_mock = MagicMock()
    tau_mock.calculate_tau_i_values = MagicMock()

    delta_tau_mock = MagicMock()
    delta_tau_mock.calculate_error_propagation_terms = MagicMock()

    tau_final_mock = MagicMock()
    tau_final_mock.calculate_tau_final = MagicMock()

    return chi_mock, tau_mock, delta_tau_mock, tau_final_mock


class CoreUnitTest(unittest.TestCase):
    def test_CanCalculateLifetime(self):
        """Can calculate lifetime"""
        chi_mock, tau_mock, delta_tau_mock, tau_final_mock = set_up_mocks()

        # Mocked return values of called functions
        chi_mock.optimize_t_hyp.return_value = 2.0
        chi_mock.optimize_coefficients.return_value = (np.array([2, 3, 1]), 2.0)

        tau_mock.calculate_tau_i_values.return_value = np.array([3, 1.66666667])

        delta_tau_mock.calculate_error_propagation_terms.return_value = np.array(
            [0.6, 0.2]
        )

        tau_final_mock.calculate_tau_final.return_value = (1.8, 0.18973666)

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.chi": chi_mock,
                "napytau.core.tau": tau_mock,
                "napytau.core.delta_tau": delta_tau_mock,
                "napytau.core.tau_final": tau_final_mock,
            },
        ):
            from napytau.core.core import calculate_lifetime

            # Mocked input data
            doppler_shifted_intensities: np.ndarray = np.array([2, 6])
            unshifted_intensities: np.ndarray = np.array([6, 10])
            delta_doppler_shifted_intensities: np.ndarray = np.array([1, 1])
            delta_unshifted_intensities: np.ndarray = np.array([1, 1])
            initial_coefficients: np.ndarray = np.array([1, 1, 1])
            distances: np.ndarray = np.array([0, 1])
            t_hyp_range: Tuple[float, float] = (-5, 5)
            weight_factor: float = 1.0
            custom_t_hyp_estimate: Optional[float] = None

            actual_result: Tuple[float, float] = calculate_lifetime(
                doppler_shifted_intensities,
                unshifted_intensities,
                delta_doppler_shifted_intensities,
                delta_unshifted_intensities,
                initial_coefficients,
                distances,
                t_hyp_range,
                weight_factor,
                custom_t_hyp_estimate,
            )

            self.assertAlmostEqual(actual_result[0], 1.8)

            self.assertAlmostEqual(actual_result[1], 0.18973666)

            self.assertEqual(len(chi_mock.optimize_t_hyp.mock_calls), 1)

            np.testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[0], np.array([2, 6])
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[1], np.array([6, 10])
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[2], np.array([1, 1])
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[3], np.array([1, 1])
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[4], np.array([1, 1, 1])
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[5], np.array([0, 1])
            )

            self.assertEqual(chi_mock.optimize_t_hyp.mock_calls[0].args[6], (-5, 5))

            self.assertEqual(chi_mock.optimize_t_hyp.mock_calls[0].args[7], 1.0)

            self.assertEqual(len(chi_mock.optimize_coefficients.mock_calls), 1)

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[0], np.array([2, 6])
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[1], np.array([6, 10])
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[2], np.array([1, 1])
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[3], np.array([1, 1])
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[4],
                np.array([1, 1, 1]),
            )

            np.testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[5], np.array([0, 1])
            )

            self.assertEqual(chi_mock.optimize_coefficients.mock_calls[0].args[6], 2.0)

            self.assertEqual(chi_mock.optimize_coefficients.mock_calls[0].args[7], 1.0)

            self.assertEqual(len(tau_mock.calculate_tau_i_values.mock_calls), 1)

            np.testing.assert_array_equal(
                tau_mock.calculate_tau_i_values.mock_calls[0].args[0], np.array([2, 6])
            )

            np.testing.assert_array_equal(
                tau_mock.calculate_tau_i_values.mock_calls[0].args[1], np.array([6, 10])
            )

            np.testing.assert_array_equal(
                tau_mock.calculate_tau_i_values.mock_calls[0].args[2], np.array([1, 1])
            )

            np.testing.assert_array_equal(
                tau_mock.calculate_tau_i_values.mock_calls[0].args[3], np.array([1, 1])
            )

            np.testing.assert_array_equal(
                tau_mock.calculate_tau_i_values.mock_calls[0].args[4],
                np.array([1, 1, 1]),
            )

            np.testing.assert_array_equal(
                tau_mock.calculate_tau_i_values.mock_calls[0].args[5], np.array([0, 1])
            )

            self.assertEqual(
                tau_mock.calculate_tau_i_values.mock_calls[0].args[6], (-5, 5)
            )

            self.assertEqual(tau_mock.calculate_tau_i_values.mock_calls[0].args[7], 1.0)

            self.assertEqual(
                tau_mock.calculate_tau_i_values.mock_calls[0].args[8], None
            )

            self.assertEqual(
                len(delta_tau_mock.calculate_error_propagation_terms.mock_calls), 1
            )

            np.testing.assert_array_equal(
                delta_tau_mock.calculate_error_propagation_terms.mock_calls[0].args[0],
                np.array([6, 10]),
            )

            np.testing.assert_array_equal(
                delta_tau_mock.calculate_error_propagation_terms.mock_calls[0].args[1],
                np.array([1, 1]),
            )

            np.testing.assert_array_equal(
                delta_tau_mock.calculate_error_propagation_terms.mock_calls[0].args[2],
                np.array([1, 1]),
            )

            np.testing.assert_array_equal(
                delta_tau_mock.calculate_error_propagation_terms.mock_calls[0].args[3],
                np.array([0, 1]),
            )

            np.testing.assert_array_equal(
                delta_tau_mock.calculate_error_propagation_terms.mock_calls[0].args[4],
                np.array([2, 3, 1]),
            )

            self.assertEqual(
                delta_tau_mock.calculate_error_propagation_terms.mock_calls[0].args[5],
                2.0,
            )

            self.assertEqual(len(tau_final_mock.calculate_tau_final.mock_calls), 1)

            np.testing.assert_array_equal(
                tau_final_mock.calculate_tau_final.mock_calls[0].args[0],
                np.array([3, 1.66666667]),
            )

            np.testing.assert_array_equal(
                tau_final_mock.calculate_tau_final.mock_calls[0].args[1],
                np.array([0.6, 0.2]),
            )
