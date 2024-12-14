import unittest
from napytau.core.core import calculate_tau_final
from numpy import ndarray
from numpy import array


class CoreUnitTest(unittest.TestCase):
    def test_calculateTauFinalForValidData(self):
        tau_i: ndarray = array([2, 4])
        delta_tau_i: ndarray = array([1, 2])
        expected_tau_final: float = 2.4
        expected_uncertainty: float = 0.894427191
        self.assertAlmostEqual(
            calculate_tau_final(tau_i, delta_tau_i)[0], expected_tau_final
        )
        self.assertAlmostEqual(
            calculate_tau_final(tau_i, delta_tau_i)[1], expected_uncertainty
        )


    def test_calculateTauFinalForEmptyInput(self):
        tau_i: ndarray = array([])
        delta_tau_i: ndarray = array([])
        expected_tau_final: float = -1
        expected_uncertainty: float = -1
        self.assertEqual(
            calculate_tau_final(tau_i, delta_tau_i)[0], expected_tau_final
        )
        self.assertEqual(
            calculate_tau_final(tau_i, delta_tau_i)[1], expected_uncertainty
        )