import unittest

from napytau.import_export.model.polynomial import Polynomial


class PolynomialUnitTest(unittest.TestCase):
    def test_raisesAnExceptionIfTheSpecifiedDegreeDoesNotMatchTheNumberOfCoefficients(self):
        """Raise an exception if the specified degree does not match the number of coefficients."""
        with self.assertRaises(Exception):
            Polynomial([1.0, 2.0, 3.0, 4.0], 2)

    def test_raisesAnExceptionIfTheSpecifiedDegreeDoesNotMatchTheNumberOfCoefficientsWhenUpdatingThePolynomial(self):
        """Raise an exception if the specified degree does not match the number of coefficients when updating the polynomial."""
        polynomial = Polynomial([1.0, 2.0, 3.0], 2)
        with self.assertRaises(Exception):
            polynomial.update([1.0, 2.0, 3.0, 4.0], 2)


if __name__ == '__main__':
    unittest.main()
