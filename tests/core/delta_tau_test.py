import unittest
from unittest.mock import MagicMock, patch
import numpy as np


def set_up_mocks() -> (MagicMock, MagicMock, MagicMock, MagicMock):
    polynomial_module_mock = MagicMock()
    polynomial_module_mock.polynomial_sum_at_measuring_times = MagicMock()
    polynomial_module_mock.differentiated_polynomial_sum_at_measuring_times = (
        MagicMock()
    )

    zeros_mock = MagicMock()
    numpy_module_mock = MagicMock()
    numpy_module_mock.zeros = zeros_mock
    numpy_module_mock.diag = MagicMock()
    numpy_module_mock.linalg.inv = MagicMock()
    numpy_module_mock.power = MagicMock()

    # used actual implementation as these are either data types or functions used for testing only
    numpy_module_mock.array = np.array
    numpy_module_mock.testing = np.testing
    numpy_module_mock.ndarray = np.ndarray
    return polynomial_module_mock, zeros_mock, numpy_module_mock


class DeltaChiUnitTests(unittest.TestCase):
    def test_canCalculateJacobianMatrixOutOfTimesAndCoefficients(self):
        """ " Can calculate Jacobian matrix out of times and coefficients."""
        polynomial_module_mock, zeros_mock, numpy_module_mock = set_up_mocks()

        zeros_mock.return_value = np.array([[0, 0], [0, 0], [0, 0]])
        polynomial_module_mock.polynomial_sum_at_measuring_times.side_effect = \
            [
            6,
            3,
            2,
            1,
        ]

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.polynomials": polynomial_module_mock,
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.delta_tau import calculate_jacobian_matrix

            coefficients = np.array([5, 4])
            times = np.array([0, 1, 2])

            jacobian_matrix = np.array([[3e8, 1e8], [3e8, 1e8], [3e8, 1e8]])

            np.testing.assert_array_equal(
                calculate_jacobian_matrix(times, coefficients), jacobian_matrix
            )

    def test_canCalculateCovianceMatrixOutOfJacobianMatrixAndWeightMatrix(self):
        """Can calculate Coviance matrix out of times and coefficients."""
        polynomial_module_mock, zeros_mock, numpy_module_mock = set_up_mocks()

        zeros_mock.return_value = np.array([[0, 0], [0, 0], [0, 0]])
        polynomial_module_mock.polynomial_sum_at_measuring_times.side_effect = [
            6,
            3,
            2,
            1,
        ]
        numpy_module_mock.diag.return_value = np.array(
            [[1 / 4, 0, 0], [0, 1 / 9, 0], [0, 0, 1 / 16]]
        )
        numpy_module_mock.linalg.inv.return_value = np.array(
            [[-0.13826047, 0.41478141], [0.41478141, -1.24434423]]
        )

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.polynomials": polynomial_module_mock,
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.delta_tau import calculate_covariance_matrix

            delta_shifted_intensities: np.array = np.array([2, 3, 4])
            times: np.array = np.array([0, 1, 2])
            coefficients = np.array([5, 4])

            expected_fit_matrix = np.array(
                [[3.81250000e16, 1.27083333e16], [1.27083333e16, 4.23611111e15]]
            )

            self.assertEqual(zeros_mock.mock_calls[0].args[0], 3)
            self.assertEqual(zeros_mock.mock_calls[0].args[1], 2)

            np.testing.assert_array_equal(
                polynomial_module_mock.polynomial_sum_at_measuring_times.mock_calls[
                    0
                ].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.polynomial_sum_at_measuring_times.mock_calls[
                    0
                ].args[1],
                np.array([5 + 1e-8, 4]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.polynomial_sum_at_measuring_times.mock_calls[
                    1
                ].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.polynomial_sum_at_measuring_times.mock_calls[
                    1
                ].args[1],
                np.array([5, 4]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.polynomial_sum_at_measuring_times.mock_calls[
                    2
                ].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.polynomial_sum_at_measuring_times.mock_calls[
                    2
                ].args[1],
                np.array([5 + 1e-8, 4 + 1e-8]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.polynomial_sum_at_measuring_times.mock_calls[
                    3
                ].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.polynomial_sum_at_measuring_times.mock_calls[
                    3
                ].args[1],
                np.array([5, 4]),
            )

            np.testing.assert_array_equal(numpy_module_mock.diag.mock_calls[0].arg[0], np.array([1/4,1/9,1/16]))

            np.testing.assert_array_equal(numpy_module_mock.linalg.inv.mock_calls[0].arg[0],np.array(
                [[3.81250000e16, 1.27083333e16], [1.27083333e16, 4.23611111e15]]
            ))

            expected_covariance_matrix: np.array = np.array(
                [[-0.13826047, 0.41478141], [0.41478141, -1.24434423]]
            )

            np.testing.assert_array_equal(
                calculate_covariance_matrix(
                    delta_shifted_intensities, times, coefficients
                ),
                expected_covariance_matrix,
            )


    def testCanCalculateGaussianErrorPropagation(self):
        """Can calculate Gaussian error propagation"""
        polynomial_module_mock, zeros_mock, numpy_module_mock, jacobian_matrix_mock = (
            set_up_mocks()
        )
        coviance_matrix_mock = MagicMock()
        coviance_matrix_mock.calculate_coviance_matrix = MagicMock()

        zeros_mock.return_value = np.zeros((1, 3))
        coviance_matrix_mock.return_value = np.array(
            [[-0.13826047, 0.41478141], [0.41478141, -1.24434423]]
        )

        polynomial_module_mock.differentiated_polynomial_sum_at_measuring_times.return_value = np.array(
            [4, 4, 4]
        )

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.delta_tau": polynomial_module_mock,
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.delta_tau import (
                calculate_gaussian_error_propagation_terms,
            )

            delta_shifted_intensities: np.array = np.array([2, 3, 4])
            times: np.array = np.array([0, 1, 2])
            coefficients = np.array([5, 4])
            delta_unshifted_intensities: np.array = np.array([5, 6, 7])
            unshifted_intensities: np.array = np.array([4, 5, 6])
            taufactor = 0.4

            expected_first_summand = np.array([1.5625, 2.25, 3.0625])
            expected_second_summand = np.array(
                [9.67745352e-02, 4.33334237e-32, 1.95968434e00]
            )
            expected_third_summand = np.array(
                [3.11086058e-02, 2.08166817e-17, -1.39988726e-01]
            )

            expected_gaussian_error_propagation = np.array(
                [1.69038314, 2.25, 4.88219561]
            )

            calculated_gaussian_error_propagation_terms = (
                calculate_gaussian_error_propagation_terms(
                    unshifted_intensities,
                    delta_shifted_intensities,
                    delta_unshifted_intensities,
                    times,
                    coefficients,
                    taufactor,
                )
            )

            np.testing.assert_array_equal(
                calculated_gaussian_error_propagation_terms,
                expected_gaussian_error_propagation,
            )


if __name__ == "__main__":
    unittest.main()
