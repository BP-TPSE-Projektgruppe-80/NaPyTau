import unittest
from napytau.core.polynomials import polynomial_sum_at_measuring_distances
from napytau.core.polynomials import differentiated_polynomial_sum_at_measuring_distances
from numpy import ndarray
from numpy import array
from numpy import testing


class PolynomialsUnitTest(unittest.TestCase):
    @staticmethod
    def test_CalculationForValidPolynomial():
        # Test for a simple quadratic polynomial: 2 + 3x + 4x^2
        distances: ndarray = array([1, 2, 3])
        coefficients: ndarray = array([2, 3, 4])
        # At x = 1: 2 + 3(1) + 4(1^2) = 9
        # At x = 2: 2 + 3(2) + 4(2^2) = 2 + 6 + 16 = 24
        # At x = 3: 2 + 3(3) + 4(3^2) = 2 + 9 + 36 = 47
        expected_result: ndarray = array([9, 24, 47])
        testing.assert_array_equal(
            polynomial_sum_at_measuring_distances(distances, coefficients), expected_result
        )

    @staticmethod
    def test_CalculationForEmptyDistanceInput():
        distances: ndarray = array([])
        coefficients: ndarray = array([2, 3, 4])
        # With an empty input array, the result should also be an empty array
        expected_result: ndarray = array([])
        testing.assert_array_equal(
            polynomial_sum_at_measuring_distances(distances, coefficients), expected_result
        )

    @staticmethod
    def test_CalculationForSingleDistanceMeasurement():
        distances: ndarray = array([2])
        coefficients: ndarray = array([1, 2])
        # Polynomial: f(x) = 1 + 2x
        # At x = 2: 1 + 2(2) = 5
        expected_result: ndarray = array([5])
        testing.assert_array_equal(
            polynomial_sum_at_measuring_distances(distances, coefficients), expected_result
        )

    @staticmethod
    def test_CalculationForSingleValuePolynomial():
        distances: ndarray = array([1, 2, 3])
        coefficients: ndarray = array([5])
        # Constant polynomial: f(x) = 5
        # All values should be 5
        expected_result: ndarray = array([5, 5, 5])
        testing.assert_array_equal(
            polynomial_sum_at_measuring_distances(distances, coefficients), expected_result
        )

    @staticmethod
    def test_CalculationForEmptyPolynomial():
        distances: ndarray = array([1, 2])
        coefficients: ndarray = array([])
        # With an empty coefficients array, the result should be an array of zeros
        # with the same length as 'distances'
        expected_result: ndarray = array([0, 0], float)
        testing.assert_array_equal(
            polynomial_sum_at_measuring_distances(distances, coefficients), expected_result
        )

    @staticmethod
    def test_DifferentiatedCalculationForValidPolynomial():
        # Test for a simple quadratic polynomial: 2 + 3x + 4x^2
        distances: ndarray = array([1, 2, 3])
        coefficients: ndarray = array([2, 3, 4])
        # The differentiated polynomial should be: 3 + 8x
        # At x = 1: 3 + 8(1) = 3 + 8 = 11
        # At x = 2: 3 + 8(2) = 3 + 16 = 19
        # At x = 3: 3 + 8(3) = 3 + 24 = 27
        expected_result: ndarray = array([11, 19, 27])
        testing.assert_array_equal(
            differentiated_polynomial_sum_at_measuring_distances(distances, coefficients),
            expected_result,
        )

    @staticmethod
    def test_DifferentiatedCalculationForEmptyDistanceInput():
        distances: ndarray = array([])
        coefficients: ndarray = array([2, 3, 4])
        # With an empty input array, the result should also be an empty array
        expected_result: ndarray = array([])
        testing.assert_array_equal(
            differentiated_polynomial_sum_at_measuring_distances(distances, coefficients),
            expected_result,
        )

    @staticmethod
    def test_DifferentiatedCalculationForSingleDistanceMeasurement():
        distances: ndarray = array([2])
        coefficients: ndarray = array([1, 2])
        # The differentiated polynomial should be: 2
        # At x = 2: 2
        expected_result: ndarray = array([2])
        testing.assert_array_equal(
            differentiated_polynomial_sum_at_measuring_distances(distances, coefficients),
            expected_result,
        )

    @staticmethod
    def test_DifferentiatedCalculationForSingleValuePolynomial():
        distances: ndarray = array([1, 2, 3])
        coefficients: ndarray = array([5])
        # The differentiated polynomial should be: 0
        # All values should therefore be 0
        expected_result: ndarray = array([0, 0, 0])
        testing.assert_array_equal(
            differentiated_polynomial_sum_at_measuring_distances(distances, coefficients),
            expected_result,
        )

    @staticmethod
    def test_DifferentiatedCalculationForEmptyPolynomial():
        distances: ndarray = array([1, 2])
        coefficients: ndarray = array([])
        # With an empty coefficients array, the result should be an array of zeros
        # with the same length as 'distances'
        expected_result: ndarray = array([0, 0])
        testing.assert_array_equal(
            differentiated_polynomial_sum_at_measuring_distances(distances, coefficients),
            expected_result,
        )


if __name__ == "__main__":
    unittest.main()
