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
    @staticmethod
    def test_canCalculateAJacobianMatrixFromTimesAndCoefficients():
        """Can calculate Jacobian matrix out of distances and coefficients."""
        polynomial_module_mock, zeros_mock, numpy_module_mock = set_up_mocks()

        zeros_mock.return_value = np.array([[0, 0], [0, 0], [0, 0]])
        polynomial_module_mock.evaluate_polynomial_at_measuring_distances.side_effect = [
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
            distances = np.array([0, 1, 2])

            jacobian_matrix = np.array([[3e8, 1e8], [3e8, 1e8], [3e8, 1e8]])

            np.testing.assert_array_equal(
                calculate_jacobian_matrix(distances, coefficients), jacobian_matrix
            )

    def test_canCalculateACovarianceMatrixFromAJacobianMatrixAndAWeightMatrix(self):
        """Can calculate Covariance matrix out of times and coefficients."""
        polynomial_module_mock, zeros_mock, numpy_module_mock = set_up_mocks()

        zeros_mock.return_value = np.array([[0, 0], [0, 0], [0, 0]])
        polynomial_module_mock.evaluate_polynomial_at_measuring_distances.side_effect = [
            6,
            3,
            2,
            1,
        ]
        numpy_module_mock.power.return_value = np.array([4, 9, 16])
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
            distances: np.array = np.array([0, 1, 2])
            coefficients = np.array([5, 4])

            np.testing.assert_array_equal(
                calculate_covariance_matrix(
                    delta_shifted_intensities, distances, coefficients
                ),
                np.array([[-0.13826047, 0.41478141], [0.41478141, -1.24434423]]),
            )

            self.assertEqual(zeros_mock.mock_calls[0].args[0], (3, 2))

            self.assertEqual(
                len(
                    polynomial_module_mock.evaluate_polynomial_at_measuring_distances.mock_calls
                ),
                4,
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                np.array([5 + 1e-8, 4]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    1
                ].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    1
                ].args[1],
                np.array([5, 4]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    2
                ].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    2
                ].args[1],
                np.array([5, 4 + 1e-8]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    3
                ].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    3
                ].args[1],
                np.array([5, 4]),
            )

            np.testing.assert_array_equal(
                numpy_module_mock.diag.mock_calls[0].args[0],
                np.array([1 / 4, 1 / 9, 1 / 16]),
            )

            np.testing.assert_allclose(
                numpy_module_mock.linalg.inv.mock_calls[0].args[0],
                np.array(
                    [[3.81250000e16, 1.27083333e16], [1.27083333e16, 4.23611111e15]]
                ),
            )

    def test_CanCalculateTheErrorPropagation(self):
        """Can calculate error propagation"""
        polynomial_module_mock, zeros_mock, numpy_module_mock = set_up_mocks()

        zeros_mock.side_effect = [
            np.array([0, 0, 0]),
            np.array([[0, 0], [0, 0], [0, 0]]),
        ]
        polynomial_module_mock.evaluate_polynomial_at_measuring_distances.side_effect = [
            6,
            3,
            2,
            1,
        ]
        numpy_module_mock.power.return_value = np.array([4, 9, 16])
        numpy_module_mock.diag.return_value = np.array(
            [[1 / 4, 0, 0], [0, 1 / 9, 0], [0, 0, 1 / 16]]
        )
        numpy_module_mock.linalg.inv.return_value = np.array(
            [[-0.13826047, 0.41478141], [0.41478141, -1.24434423]]
        )

        numpy_module_mock.power.side_effect = [
            np.array([25, 36, 49]),
            np.array([16, 16, 16]),
            np.array([4, 9, 16]),
            np.array([1, 1, 1]),
            np.array([1, 1, 1]),
            np.array([1, 1, 1]),
            np.array([0, 1, 2]),
            np.array([0, 1, 2]),
            np.array([1, 1, 1]),
            np.array([0, 1, 2]),
            np.array([0, 1, 2]),
            np.array([16, 25, 36]),
            np.array([256, 256, 256]),
            np.array([2.60475853e26, 2.60475853e26, 2.60475853e26]),
            np.array([64, 64, 64]),
        ]

        polynomial_module_mock.evaluate_differentiated_polynomial_at_measuring_distances.return_value = np.array(
            [4, 4, 4]
        )

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.polynomials": polynomial_module_mock,
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.delta_tau import (
                calculate_error_propagation_terms,
            )

            delta_shifted_intensities: np.array = np.array([2, 3, 4])
            distances: np.array = np.array([0, 1, 2])
            coefficients: np.array = np.array([5, 4])
            delta_unshifted_intensities: np.array = np.array([5, 6, 7])
            unshifted_intensities: np.array = np.array([4, 5, 6])
            taufactor = 0.4

            calculated_error_propagation_terms = calculate_error_propagation_terms(
                unshifted_intensities,
                delta_shifted_intensities,
                delta_unshifted_intensities,
                distances,
                coefficients,
                taufactor,
            )

            np.testing.assert_array_equal(
                polynomial_module_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                polynomial_module_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                np.array([5, 4]),
            )

            self.assertEqual(
                len(numpy_module_mock.power.mock_calls),
                15,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[0].args[0],
                np.array([5, 6, 7]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[0].args[1],
                2,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[1].args[0],
                np.array([4, 4, 4]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[1].args[1],
                2,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[2].args[0],
                np.array([2, 3, 4]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[2].args[1],
                2,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[3].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[3].args[1],
                0,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[4].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[4].args[1],
                0,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[5].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[5].args[1],
                0,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[6].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[6].args[1],
                1,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[7].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[7].args[1],
                1,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[8].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[8].args[1],
                0,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[9].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[9].args[1],
                1,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[10].args[0],
                np.array([0, 1, 2]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[10].args[1],
                1,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[11].args[0],
                np.array([4, 5, 6]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[11].args[1],
                2,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[12].args[0],
                np.array([4, 4, 4]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[12].args[1],
                4,
            )
            np.testing.assert_allclose(
                numpy_module_mock.power.mock_calls[13].args[0],
                np.array([-0.13826, -0.553042, -3.456512]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[13].args[1],
                2,
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[14].args[0],
                np.array([4, 4, 4]),
            )
            np.testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[14].args[1],
                3,
            )

            gaussian_error_propagation_terms = np.array(
                [1.627974e25, 2.543710e25, 3.662942e25]
            )

            np.testing.assert_allclose(
                calculated_error_propagation_terms,
                gaussian_error_propagation_terms,
            )


if __name__ == "__main__":
    unittest.main()
