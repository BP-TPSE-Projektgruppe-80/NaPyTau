import unittest
from napytau.core.polynomials import polynomial_sum_at_measuring_times
from numpy import array
from numpy import testing


class PolynomialsUnitTest(unittest.TestCase):
    @staticmethod
    def test_correctCalculationForValidPolynomial():
        # Test for a simple quadratic polynomial: 2 + 3x + 4x^2
        times: array = [1, 2, 3]
        coefficients: array = [2, 3, 4]
        # At x = 1: 2 + 3(1) + 4(1^2) = 9
        # At x = 2: 2 + 3(2) + 4(2^2) = 2 + 6 + 16 = 24
        # At x = 3: 2 + 3(3) + 4(3^2) = 2 + 9 + 36 = 47
        expected_result: array = [9, 24, 47]
        testing.assert_array_equal(
            polynomial_sum_at_measuring_times(times, coefficients), expected_result)

    @staticmethod
    def test_correctCalculationForEmptyTimeInput():
        times: array = []
        coefficients: array = [2, 3, 4]
        # With an empty input array, the result should also be an empty array
        expected_result: array = []
        testing.assert_array_equal(
            polynomial_sum_at_measuring_times(times, coefficients), expected_result)

    @staticmethod
    def test_correctCalculationForSingleTimeMeasurement():
        times: array = [2]
        coefficients: array = [1, 2]
        # Polynomial: f(x) = 1 + 2x
        # At x = 2: 1 + 2(2) = 5
        expected_result: array = [5]
        testing.assert_array_equal(
            polynomial_sum_at_measuring_times(times, coefficients), expected_result)

    @staticmethod
    def test_correctCalculationForSingleValuePolynomial():
        times: array = [1, 2, 3]
        coefficients: array = [5]
        # Constant polynomial: f(x) = 5
        # All values should be 5
        expected_result: array = [5, 5, 5]
        testing.assert_array_equal(
            polynomial_sum_at_measuring_times(times, coefficients), expected_result)

    @staticmethod
    def test_correctCalculationForEmptyPolynomial():
        times: array = [1, 2]
        coefficients: array = []
        # With an empty coefficients array, the result should be an array of zeros
        # with the same length as 'times'
        expected_result: array = [0, 0]
        testing.assert_array_equal(
            polynomial_sum_at_measuring_times(times, coefficients), expected_result)



if __name__ == '__main__':
    unittest.main()