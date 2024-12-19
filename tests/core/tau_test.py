import unittest
from unittest.mock import MagicMock, patch
from numpy import ndarray
from numpy import array
from numpy import testing
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
        chi_mock.optimize_coefficients.return_value: Tuple[ndarray, float] = (
            array([2, 3, 1]),
            0,
        )
        chi_mock.optimize_t_hyp.return_value: float = 2.0
        polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.return_value: ndarray = array(
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

            # Mocked input data
            doppler_shifted_intensities: ndarray = array([2, 6])
            unshifted_intensities: ndarray = array([6, 10])
            delta_doppler_shifted_intensities: ndarray = array([1, 1])
            delta_unshifted_intensities: ndarray = array([1, 1])
            initial_coefficients: ndarray = array([1, 1, 1])
            distances: ndarray = array([0, 1])
            t_hyp_range: (float, float) = (-5, 5)
            weight_factor: float = 1.0

            # Expected result
            expected_tau: ndarray = array([3, 1.6666667])

            testing.assert_array_almost_equal(
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

            testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[0],
                (array([2, 6])),
            )

            testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[1],
                (array([6, 10])),
            )

            testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[2],
                (array([1, 1])),
            )

            testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[3],
                (array([1, 1])),
            )

            testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[4],
                (array([1, 1, 1])),
            )

            testing.assert_array_equal(
                chi_mock.optimize_coefficients.mock_calls[0].args[5],
                (array([0, 1])),
            )

            self.assertEqual(
                chi_mock.optimize_coefficients.mock_calls[0].args[6],
                2.0,
            )

            self.assertEqual(chi_mock.optimize_coefficients.mock_calls[0].args[7], 1.0)


            self.assertEqual(len(chi_mock.optimize_t_hyp.mock_calls), 1)

            testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[0],
                (array([2, 6])),
            )

            testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[1],
                (array([6, 10])),
            )

            testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[2],
                (array([1, 1])),
            )

            testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[3],
                (array([1, 1])),
            )

            testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[4],
                (array([1, 1, 1])),
            )

            testing.assert_array_equal(
                chi_mock.optimize_t_hyp.mock_calls[0].args[5],
                (array([0, 1])),
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

            testing.assert_array_equal(
                polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[0],
                (array([0, 1])),
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (array([2, 3, 1])),
            )
