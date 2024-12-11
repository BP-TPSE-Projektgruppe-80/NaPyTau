import unittest
from unittest.mock import MagicMock, patch
import numpy as np

def set_up_mocks() -> (MagicMock, MagicMock, MagicMock):
    polynomial_module_mock = MagicMock()
    polynomial_module_mock.polynomial_sum_at_measuring_times = MagicMock()
    zeros_mock = MagicMock()
    numpy_module_mock = MagicMock()
    numpy_module_mock.array = np.array
    numpy_module_mock.zeros = zeros_mock
    numpy_module_mock.testing = np.testing
    return polynomial_module_mock, zeros_mock, numpy_module_mock

class DeltaChiUnitTests(unittest.TestCase):
    def test_canCalculateJacobianMatrixOutOfTimesAndCoefficients(self):
        """" Can calculate Jacobian matrix out of times and coefficients. """
        polynomial_module_mock, zeros_mock, numpy_module_mock = set_up_mocks()

        zeros_mock.return_value = np.zeros((3, 2))
        polynomial_module_mock.polynomial_sum_at_measuring_times.side_effect = \
            [6, 3, 2, 1]

        with patch.dict(
                "sys.modules",
                {
                    "napytau.core.polynomials": polynomial_module_mock,
                    "numpy": numpy_module_mock
                },
        ):
            from napytau.core.delta_tau import calculate_jacobian_matrix

            coefficients = np.array([5, 4])
            times = np.array([0, 1, 2])

            jacobian_matrix = np.array([[3e8,1e8],
                               [3e8,1e8],
                               [3e8,1e8]])

            np.testing.assert_array_equal(calculate_jacobian_matrix(times,
                                                                    coefficients),
                                          jacobian_matrix)


if __name__ == '__main__':
    unittest.main()
