import unittest
from unittest.mock import MagicMock, patch
from napytau.core.errors.polynomial_coefficient_error import (
    PolynomialCoefficientError,
)
import numpy as np


def set_up_mocks() -> MagicMock:
    numpy_module_mock = MagicMock()
    numpy_module_mock.power = MagicMock()
    numpy_module_mock.zeros_like = MagicMock()

    return numpy_module_mock


class PolynomialsUnitTest(unittest.TestCase):
    @staticmethod
    def test_CanEvaluateAValidPolynomialAtMeasuringDistances():
        """Can evaluate a valid polynomial at measuring distances."""
        numpy_module_mock = set_up_mocks()

        # Mocked return values of called functions
        numpy_module_mock.power.side_effect = [
            np.array([1, 1, 1]),
            np.array([1, 2, 3]),
            np.array([1, 4, 9]),
        ]
        numpy_module_mock.zeros_like.return_value = np.array([0, 0, 0])

        with patch.dict(
            "sys.modules",
            {
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.polynomials import (
                evaluate_polynomial_at_measuring_distances,
            )

            # Test for a simple quadratic polynomial: 2 + 3x + 4x^2
            distances: np.ndarray = np.array([1, 2, 3])
            coefficients: np.ndarray = np.array([2, 3, 4])
            # At x = 1: 2 + 3(1) + 4(1^2) = 9
            # At x = 2: 2 + 3(2) + 4(2^2) = 2 + 6 + 16 = 24
            # At x = 3: 2 + 3(3) + 4(3^2) = 2 + 9 + 36 = 47
            expected_result: np.ndarray = np.array([9, 24, 47])
            np.testing.assert_array_equal(
                evaluate_polynomial_at_measuring_distances(distances, coefficients),
                expected_result,
            )

    @staticmethod
    def test_CanEvaluateAPolynomialAtMeasuringDistancesForEmptyDistanceInput():
        """Can evaluate a polynomial at measuring distances for empty distance input."""
        numpy_module_mock = set_up_mocks()

        # Mocked return values of called functions
        numpy_module_mock.power.side_effect = [np.array([]), np.array([]), np.array([])]
        numpy_module_mock.zeros_like.return_value = np.array([])

        with patch.dict(
            "sys.modules",
            {
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.polynomials import (
                evaluate_polynomial_at_measuring_distances,
            )

            distances: np.ndarray = np.array([])
            coefficients: np.ndarray = np.array([2, 3, 4])
            # With an empty input array, the result should also be an empty array
            expected_result: np.ndarray = np.array([])
            np.testing.assert_array_equal(
                evaluate_polynomial_at_measuring_distances(distances, coefficients),
                expected_result,
            )

    @staticmethod
    def test_CanEvaluateAPolynomialAtMeasuringDistancesForASingleDistance():
        """Can evaluate a polynomial at measuring distances for a single distance."""
        numpy_module_mock = set_up_mocks()

        # Mocked return values of called functions
        numpy_module_mock.power.side_effect = [
            np.array([1]),
            np.array([2]),
            np.array([4]),
        ]
        numpy_module_mock.zeros_like.return_value = np.array([0])

        with patch.dict(
            "sys.modules",
            {
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.polynomials import (
                evaluate_polynomial_at_measuring_distances,
            )

            distances: np.ndarray = np.array([2])
            coefficients: np.ndarray = np.array([1, 2])
            # Polynomial: f(x) = 1 + 2x
            # At x = 2: 1 + 2(2) = 5
            expected_result: np.ndarray = np.array([5])
            np.testing.assert_array_equal(
                evaluate_polynomial_at_measuring_distances(distances, coefficients),
                expected_result,
            )

    @staticmethod
    def test_CanEvaluateAPolynomialOfDegreeZeroAtMeasuringDistances():
        """Can evaluate a polynomial of degree zero at measuring distances."""
        numpy_module_mock = set_up_mocks()

        # Mocked return values of called functions
        numpy_module_mock.power.side_effect = [
            np.array([1, 1, 1]),
            np.array([1, 2, 3]),
            np.array([1, 4, 9]),
        ]
        numpy_module_mock.zeros_like.return_value = np.array([0, 0, 0])

        with patch.dict(
            "sys.modules",
            {
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.polynomials import (
                evaluate_polynomial_at_measuring_distances,
            )

            distances: np.ndarray = np.array([1, 2, 3])
            coefficients: np.ndarray = np.array([5])
            # Constant polynomial: f(x) = 5
            # All values should be 5
            expected_result: np.ndarray = np.array([5, 5, 5])
            np.testing.assert_array_equal(
                evaluate_polynomial_at_measuring_distances(distances, coefficients),
                expected_result,
            )

    def test_EvaluatePolynomialRaisesAPolynomialCoefficientErrorForAnEmptyCoefficientArray(
        self,
    ):
        """Evaluate polynomial raises a polynomial coefficient error for an empty coefficient array."""

        from napytau.core.polynomials import evaluate_polynomial_at_measuring_distances

        distances: np.ndarray = np.array([1, 2])
        coefficients: np.ndarray = np.array([])
        # With an empty coefficients array, the function should throw a polynomial
        # coefficient error.
        with self.assertRaises(PolynomialCoefficientError):
            evaluate_polynomial_at_measuring_distances(distances, coefficients)

    @staticmethod
    def test_CanEvaluateAValidDifferentiatedPolynomialAtMeasuringDistances():
        """Can evaluate a valid differentiated polynomial at measuring distances."""
        numpy_module_mock = set_up_mocks()

        # Mocked return values of called functions
        numpy_module_mock.power.side_effect = [np.array([1, 1, 1]), np.array([1, 2, 3])]
        numpy_module_mock.zeros_like.return_value = np.array([0, 0, 0])

        with patch.dict(
            "sys.modules",
            {
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.polynomials import (
                evaluate_differentiated_polynomial_at_measuring_distances,
            )

            # Test for a simple quadratic polynomial: 2 + 3x + 4x^2
            distances: np.ndarray = np.array([1, 2, 3])
            coefficients: np.ndarray = np.array([2, 3, 4])
            # The differentiated polynomial should be: 3 + 8x
            # At x = 1: 3 + 8(1) = 3 + 8 = 11
            # At x = 2: 3 + 8(2) = 3 + 16 = 19
            # At x = 3: 3 + 8(3) = 3 + 24 = 27
            expected_result: np.ndarray = np.array([11, 19, 27])
            np.testing.assert_array_equal(
                evaluate_differentiated_polynomial_at_measuring_distances(
                    distances, coefficients
                ),
                expected_result,
            )

    @staticmethod
    def test_CanEvaluateADifferentiatedPolynomialAtMeasuringDistancesForEmptyDistanceInput():
        """Can evaluate a differentiated polynomial at measuring distances for empty distance input."""
        numpy_module_mock = set_up_mocks()

        # Mocked return values of called functions
        numpy_module_mock.power.side_effect = [np.array([]), np.array([])]
        numpy_module_mock.zeros_like.return_value = np.array([])

        with patch.dict(
            "sys.modules",
            {
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.polynomials import (
                evaluate_differentiated_polynomial_at_measuring_distances,
            )

            distances: np.ndarray = np.array([])
            coefficients: np.ndarray = np.array([2, 3, 4])
            # With an empty input array, the result should also be an empty array
            expected_result: np.ndarray = np.array([])
            np.testing.assert_array_equal(
                evaluate_differentiated_polynomial_at_measuring_distances(
                    distances, coefficients
                ),
                expected_result,
            )

    @staticmethod
    def test_CanEvaluateADifferentiatedPolynomialAtMeasuringDistancesForSingleDistanceMeasurement():
        """Can evaluate a differentiated polynomial at measuring distances for single distance measurement."""
        numpy_module_mock = set_up_mocks()

        # Mocked return values of called functions
        numpy_module_mock.power.side_effect = [np.array([1]), np.array([2])]
        numpy_module_mock.zeros_like.return_value = np.array([0])

        with patch.dict(
            "sys.modules",
            {
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.polynomials import (
                evaluate_differentiated_polynomial_at_measuring_distances,
            )

            distances: np.ndarray = np.array([2])
            coefficients: np.ndarray = np.array([1, 2])
            # The differentiated polynomial should be: 2
            # At x = 2: 2
            expected_result: np.ndarray = np.array([2])
            np.testing.assert_array_equal(
                evaluate_differentiated_polynomial_at_measuring_distances(
                    distances, coefficients
                ),
                expected_result,
            )

    @staticmethod
    def test_CanEvaluateADifferentiatedPolynomialOfDegreeZeroAtMeasuringDistances():
        """Can evaluate a differentiated polynomial of degree zero at measuring distances."""
        numpy_module_mock = set_up_mocks()

        # Mocked return values of called functions
        numpy_module_mock.power.side_effect = [np.array([1, 1, 1]), np.array([1, 2, 3])]
        numpy_module_mock.zeros_like.return_value = np.array([0, 0, 0])

        with patch.dict(
            "sys.modules",
            {
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.polynomials import (
                evaluate_differentiated_polynomial_at_measuring_distances,
            )

            distances: np.ndarray = np.array([1, 2, 3])
            coefficients: np.ndarray = np.array([5])
            # The differentiated polynomial should be: 0
            # All values should therefore be 0
            expected_result: np.ndarray = np.array([0, 0, 0])
            np.testing.assert_array_equal(
                evaluate_differentiated_polynomial_at_measuring_distances(
                    distances, coefficients
                ),
                expected_result,
            )

    def test_EvaluateDifferentiatedPolynomialRaisesAPolynomialCoefficientErrorForAnEmptyCoefficientArray(
        self,
    ):
        """Evaluate differentiated polynomial raises a polynomial coefficient error for an empty coefficient array."""
        from napytau.core.polynomials import (
            evaluate_differentiated_polynomial_at_measuring_distances,
        )

        distances: np.ndarray = np.array([1, 2])
        coefficients: np.ndarray = np.array([])
        # With an empty coefficients array, the function should throw a polynomial
        # coefficient error.
        with self.assertRaises(PolynomialCoefficientError):
            evaluate_differentiated_polynomial_at_measuring_distances(
                distances, coefficients
            )


if __name__ == "__main__":
    unittest.main()
