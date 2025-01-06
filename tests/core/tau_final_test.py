import unittest
from unittest.mock import MagicMock, patch
import numpy as np


def set_up_mocks() -> MagicMock:
    numpy_module_mock = MagicMock()
    numpy_module_mock.power = MagicMock()
    numpy_module_mock.sum = MagicMock()
    numpy_module_mock.sqrt = MagicMock()
    return numpy_module_mock


class TauFinalUnitTest(unittest.TestCase):
    def test_calculateTauFinalForValidData(self):
        """Calculate tau_final for valid data."""
        numpy_module_mock = set_up_mocks()

        # Mocked return values of called functions
        numpy_module_mock.power.return_value: np.ndarray = np.array([1, 4])
        numpy_module_mock.sum.side_effect = [3, 1.25, 1.25]
        numpy_module_mock.sqrt.return_value: float = 0.894427191

        with patch.dict(
            "sys.modules",
            {
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.tau_final import calculate_tau_final

            tau_i: np.ndarray = np.array([2, 4])
            delta_tau_i: np.ndarray = np.array([1, 2])

            tau_final: (float, float) = calculate_tau_final(tau_i, delta_tau_i)

            expected_tau_final: float = 2.4
            expected_uncertainty: float = 0.894427191

            self.assertAlmostEqual(tau_final[0], expected_tau_final)
            self.assertAlmostEqual(tau_final[1], expected_uncertainty)

    def test_calculateTauFinalForEmptyInput(self):
        """Calculate tau_final for empty input."""
        numpy_module_mock = set_up_mocks()

        # Mocked return values of called functions
        numpy_module_mock.power.return_value: np.ndarray = np.array([])
        numpy_module_mock.sum.side_effect = [0, 0, 0, 0]
        numpy_module_mock.sqrt.return_value: float = 0

        with patch.dict(
            "sys.modules",
            {
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.tau_final import calculate_tau_final

            tau_i:np.ndarray = np.array([])
            delta_tau_i: np.ndarray = np.array([])

            tau_final: (float, float) = calculate_tau_final(tau_i, delta_tau_i)

            expected_tau_final: float = -1
            expected_uncertainty: float = -1

            self.assertEqual(tau_final[0], expected_tau_final)
            self.assertEqual(tau_final[1], expected_uncertainty)
