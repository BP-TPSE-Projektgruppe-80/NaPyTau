import unittest
from unittest.mock import MagicMock, patch
from numpy import array
from numpy import ndarray
from numpy import testing
from scipy.optimize import OptimizeResult
from typing import Tuple


def set_up_mocks() -> (MagicMock, MagicMock, MagicMock):
    polynomials_mock = MagicMock()
    polynomials_mock.polynomial_sum_at_measuring_times = MagicMock()
    polynomials_mock.differentiated_polynomial_sum_at_measuring_times = MagicMock()

    numpy_module_mock = MagicMock()
    numpy_module_mock.sum = MagicMock()
    numpy_module_mock.power = MagicMock()
    numpy_module_mock.mean = MagicMock()

    scipy_optimize_module_mock = MagicMock()
    scipy_optimize_module_mock.minimize = MagicMock()

    return polynomials_mock, numpy_module_mock, scipy_optimize_module_mock


class ChiUnitTest(unittest.TestCase):
    def test_CanCalculateChiForValidData(self):
        """Can calculate chi for valid data"""
        polynomials_mock, numpy_module_mock, scipy_optimize_module_mock = set_up_mocks()

        polynomials_mock.evaluate_polynomial_at_measuring_distances.return_value = (
            array([5, 15, 57])
        )
        polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.return_value = array(
            [4, 20, 72]
        )

        numpy_module_mock.sum.return_value = 628.3486168
        numpy_module_mock.power.side_effect = [
            array([4, 18.77777778, 182.25]),
            array([0.64, 34.02777778, 388.65306122]),
        ]

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.polynomials": polynomials_mock,
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.chi import chi_squared_fixed_t

            doppler_shifted_intensities: ndarray = array([1, 2, 3])
            unshifted_intensities: ndarray = array([4, 5, 6])
            delta_doppler_shifted_intensities: ndarray = array([2, 3, 4])
            delta_unshifted_intensities: ndarray = array([5, 6, 7])
            coefficients: ndarray = array([5, 4, 3, 2, 1])
            distances: ndarray = array([0, 1, 2])
            t_hyp: float = 2.0
            weight_factor: float = 1.0

            expected_result: float = 628.3486168

            self.assertAlmostEqual(
                chi_squared_fixed_t(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    coefficients,
                    distances,
                    t_hyp,
                    weight_factor,
                ),
                expected_result,
            )

            self.assertEqual(
                len(
                    polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls
                ),
                1,
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[0],
                (array([0, 1, 2])),
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (array([5, 4, 3, 2, 1])),
            )

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
                (array([0, 1, 2])),
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (array([5, 4, 3, 2, 1])),
            )

            self.assertEqual(
                len(numpy_module_mock.sum.mock_calls),
                1,
            )

            testing.assert_array_almost_equal(
                numpy_module_mock.sum.mock_calls[0].args[0],
                (array([4.64, 52.80555556, 570.90306122])),
            )

            self.assertEqual(
                len(numpy_module_mock.power.mock_calls),
                2,
            )

            testing.assert_array_almost_equal(
                numpy_module_mock.power.mock_calls[0].args[0],
                (array([-2, -4.33333333, -13.5])),
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[0].args[1],
                2,
            )

            testing.assert_array_almost_equal(
                numpy_module_mock.power.mock_calls[1].args[0],
                (array([-0.8, -5.83333333, -19.71428571])),
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[1].args[1],
                2,
            )

    def test_CanHandleEmptyDataArraysForChiCalculation(self):
        """Can handle empty data arrays for chi calculation"""
        polynomials_mock, numpy_module_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return values of called functions
        polynomials_mock.evaluate_polynomial_at_measuring_distances.return_value = (
            array([])
        )
        polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.return_value = array(
            []
        )

        numpy_module_mock.sum.return_value = 0
        numpy_module_mock.power.side_effect = [array([]), array([])]

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.polynomials": polynomials_mock,
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.chi import chi_squared_fixed_t

            doppler_shifted_intensities: ndarray = array([])
            unshifted_intensities: ndarray = array([])
            delta_doppler_shifted_intensities: ndarray = array([])
            delta_unshifted_intensities: ndarray = array([])
            coefficients: ndarray = array([])
            distances: ndarray = array([])
            t_hyp: float = 2.0
            weight_factor: float = 1.0

            expected_result: float = 0

            self.assertEqual(
                chi_squared_fixed_t(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    coefficients,
                    distances,
                    t_hyp,
                    weight_factor,
                ),
                expected_result,
            )

            self.assertEqual(
                len(
                    polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls
                ),
                1,
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[0],
                (array([])),
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (array([])),
            )

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
                (array([])),
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (array([])),
            )

            self.assertEqual(
                len(numpy_module_mock.sum.mock_calls),
                1,
            )

            testing.assert_array_equal(
                numpy_module_mock.sum.mock_calls[0].args[0],
                array([]),
            )

            self.assertEqual(
                len(numpy_module_mock.power.mock_calls),
                2,
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[0].args[0],
                (array([])),
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[0].args[1],
                2,
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[1].args[0],
                (array([])),
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[1].args[1],
                2,
            )

    def test_CanCalculateChiForASingleDatapoint(self):
        """Can calculate chi for a single datapoint"""
        polynomials_mock, numpy_module_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return values of called functions
        polynomials_mock.evaluate_polynomial_at_measuring_distances.return_value = (
            array([57])
        )
        polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.return_value = array(
            [72]
        )

        numpy_module_mock.sum.return_value = 1608.69444444
        numpy_module_mock.power.side_effect = [array([348.44444444]), array([1260.25])]

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.polynomials": polynomials_mock,
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.chi import chi_squared_fixed_t

            doppler_shifted_intensities: ndarray = array([1])
            unshifted_intensities: ndarray = array([2])
            delta_doppler_shifted_intensities: ndarray = array([3])
            delta_unshifted_intensities: ndarray = array([4])
            coefficients: ndarray = array([5, 4, 3, 2, 1])
            distances: ndarray = array([2])
            t_hyp: float = 2.0
            weight_factor: float = 1.0

            expected_result: float = 1608.69444444

            self.assertAlmostEqual(
                chi_squared_fixed_t(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    coefficients,
                    distances,
                    t_hyp,
                    weight_factor,
                ),
                expected_result,
            )

            self.assertEqual(
                len(
                    polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls
                ),
                1,
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[0],
                (array([2])),
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (array([5, 4, 3, 2, 1])),
            )

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
                (array([2])),
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (array([5, 4, 3, 2, 1])),
            )

            self.assertEqual(
                len(numpy_module_mock.sum.mock_calls),
                1,
            )

            testing.assert_array_almost_equal(
                numpy_module_mock.sum.mock_calls[0].args[0],
                (array([1608.69444444])),
            )

            self.assertEqual(
                len(numpy_module_mock.power.mock_calls),
                2,
            )

            testing.assert_array_almost_equal(
                numpy_module_mock.power.mock_calls[0].args[0],
                (array([-18.66666667])),
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[0].args[1],
                2,
            )

            testing.assert_array_almost_equal(
                numpy_module_mock.power.mock_calls[1].args[0],
                (array([-35.5])),
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[1].args[1],
                2,
            )

    def test_CanCalculateChiIfTheDenominatorIsZero(self):
        """Can calculate chi if the denominator is zero."""
        polynomials_mock, numpy_module_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return values of called functions
        polynomials_mock.evaluate_polynomial_at_measuring_distances.return_value = (
            array([5, 15])
        )
        polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.return_value = array(
            [4, 20]
        )

        numpy_module_mock.sum.return_value = float("inf")
        numpy_module_mock.power.side_effect = [
            array([float("inf"), 169]),
            array([float("inf"), 1296]),
        ]

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.polynomials": polynomials_mock,
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.chi import chi_squared_fixed_t

            doppler_shifted_intensities: ndarray = array([1, 2])
            unshifted_intensities: ndarray = array([3, 4])
            delta_doppler_shifted_intensities: ndarray = array([0, 1])
            delta_unshifted_intensities: ndarray = array([0, 1])
            coefficients: ndarray = array([5, 4, 3, 2, 1])
            distances: ndarray = array([0, 1])
            t_hyp: float = 2.0
            weight_factor: float = 1.0

            expected_result: float = float("inf")

            self.assertAlmostEqual(
                chi_squared_fixed_t(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    coefficients,
                    distances,
                    t_hyp,
                    weight_factor,
                ),
                expected_result,
            )

            self.assertEqual(
                len(
                    polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls
                ),
                1,
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[0],
                (array([0, 1])),
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (array([5, 4, 3, 2, 1])),
            )

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
                (array([5, 4, 3, 2, 1])),
            )

            self.assertEqual(
                len(numpy_module_mock.sum.mock_calls),
                1,
            )

            testing.assert_array_equal(
                numpy_module_mock.sum.mock_calls[0].args[0],
                (array([float("inf"), 1465])),
            )

            self.assertEqual(
                len(numpy_module_mock.power.mock_calls),
                2,
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[0].args[0],
                (array([-float("inf"), -13])),
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[0].args[1],
                2,
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[1].args[0],
                (array([-float("inf"), -36])),
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[1].args[1],
                2,
            )

    def test_CanCalculateChiForNegativeValues(self):
        """Can calculate chi for negative values"""
        polynomials_mock, numpy_module_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return values of called functions
        polynomials_mock.evaluate_polynomial_at_measuring_distances.return_value = (
            array([-5, -5])
        )
        polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.return_value = array(
            [-4, -4]
        )

        numpy_module_mock.sum.return_value = 22.02777778
        numpy_module_mock.power.side_effect = [
            array([16, 2.25]),
            array([2.77777778, 1]),
        ]

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.polynomials": polynomials_mock,
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.chi import chi_squared_fixed_t

            doppler_shifted_intensities: ndarray = array([-1, -2])
            unshifted_intensities: ndarray = array([-3, -4])
            delta_doppler_shifted_intensities: ndarray = array([1, 2])
            delta_unshifted_intensities: ndarray = array([3, 4])
            coefficients: ndarray = array([-5, -4, 3, 2, -1])
            distances: ndarray = array([0, 1])
            t_hyp: float = 2.0
            weight_factor: float = 1.0

            expected_result: float = 22.02777778

            self.assertAlmostEqual(
                chi_squared_fixed_t(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    coefficients,
                    distances,
                    t_hyp,
                    weight_factor,
                ),
                expected_result,
            )

            self.assertEqual(
                len(
                    polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls
                ),
                1,
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[0],
                (array([0, 1])),
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (array([-5, -4, 3, 2, -1])),
            )

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
                (array([-5, -4, 3, 2, -1])),
            )

            self.assertEqual(
                len(numpy_module_mock.sum.mock_calls),
                1,
            )

            testing.assert_array_almost_equal(
                numpy_module_mock.sum.mock_calls[0].args[0],
                (array([18.77777778, 3.25])),
            )

            self.assertEqual(
                len(numpy_module_mock.power.mock_calls),
                2,
            )

            testing.assert_array_almost_equal(
                numpy_module_mock.power.mock_calls[0].args[0],
                (array([4, 1.5])),
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[0].args[1],
                2,
            )

            testing.assert_array_almost_equal(
                numpy_module_mock.power.mock_calls[1].args[0],
                (array([1.66666667, 1])),
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[1].args[1],
                2,
            )

    def test_CanCalculateChiForAWeightFactorOfZero(self):
        """Can calculate chi for a weight factor of zero"""
        polynomials_mock, numpy_module_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return values of called functions
        polynomials_mock.evaluate_polynomial_at_measuring_distances.return_value = (
            array([5, 15, 57])
        )
        polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.return_value = array(
            [4, 20, 72]
        )

        numpy_module_mock.sum.return_value = 205.02777778
        numpy_module_mock.power.side_effect = [
            array([4, 18.77777778, 182.25]),
            array([0.64, 34.02777778, 388.65306122]),
        ]

        with patch.dict(
            "sys.modules",
            {
                "napytau.core.polynomials": polynomials_mock,
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.chi import chi_squared_fixed_t

            doppler_shifted_intensities: ndarray = array([1, 2, 3])
            unshifted_intensities: ndarray = array([4, 5, 6])
            delta_doppler_shifted_intensities: ndarray = array([2, 3, 4])
            delta_unshifted_intensities: ndarray = array([5, 6, 7])
            coefficients: ndarray = array([5, 4, 3, 2, 1])
            distances: ndarray = array([0, 1, 2])
            t_hyp: float = 2.0
            weight_factor: float = 0.0

            expected_result: float = 205.02777778

            self.assertAlmostEqual(
                chi_squared_fixed_t(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    coefficients,
                    distances,
                    t_hyp,
                    weight_factor,
                ),
                expected_result,
            )

            self.assertEqual(
                len(
                    polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls
                ),
                1,
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[0],
                (array([0, 1, 2])),
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (array([5, 4, 3, 2, 1])),
            )

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
                (array([0, 1, 2])),
            )

            testing.assert_array_equal(
                polynomials_mock.evaluate_differentiated_polynomial_at_measuring_distances.mock_calls[
                    0
                ].args[1],
                (array([5, 4, 3, 2, 1])),
            )

            self.assertEqual(
                len(numpy_module_mock.sum.mock_calls),
                1,
            )

            testing.assert_array_equal(
                numpy_module_mock.sum.mock_calls[0].args[0],
                (array([4, 18.77777778, 182.25])),
            )

            self.assertEqual(
                len(numpy_module_mock.power.mock_calls),
                2,
            )

            testing.assert_array_almost_equal(
                numpy_module_mock.power.mock_calls[0].args[0],
                (array([-2, -4.33333333, -13.5])),
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[0].args[1],
                2,
            )

            testing.assert_array_almost_equal(
                numpy_module_mock.power.mock_calls[1].args[0],
                (array([-0.8, -5.83333333, -19.71428571])),
            )

            testing.assert_array_equal(
                numpy_module_mock.power.mock_calls[1].args[1],
                2,
            )

    def test_CanOptimizePolynomialCoefficients(self):
        """Can optimize polynomial coefficients"""
        polynomials_mock, numpy_module_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return value of called function
        scipy_optimize_module_mock.optimize.minimize.return_value = OptimizeResult(
            x=[2, 3, 1], fun=0.0
        )

        with patch.dict(
            "sys.modules",
            {
                "scipy": scipy_optimize_module_mock,
            },
        ):
            from napytau.core.chi import optimize_coefficients

            doppler_shifted_intensities: ndarray = array([2, 6])
            unshifted_intensities: ndarray = array([6, 10])
            delta_doppler_shifted_intensities: ndarray = array([1, 1])
            delta_unshifted_intensities: ndarray = array([1, 1])
            initial_coefficients: ndarray = array([1, 1, 1])
            distances: ndarray = array([0, 1])
            t_hyp: float = 2.0
            weight_factor: float = 1.0

            expected_chi: float = 0.0
            expected_coefficients: ndarray = array([2, 3, 1])

            actual_coefficients: ndarray
            actual_chi: float
            actual_coefficients, actual_chi = optimize_coefficients(
                doppler_shifted_intensities,
                unshifted_intensities,
                delta_doppler_shifted_intensities,
                delta_unshifted_intensities,
                initial_coefficients,
                distances,
                t_hyp,
                weight_factor,
            )

            self.assertAlmostEqual(actual_chi, expected_chi)
            testing.assert_array_almost_equal(
                actual_coefficients, expected_coefficients
            )

            self.assertEqual(
                len(scipy_optimize_module_mock.optimize.minimize.mock_calls), 1
            )

            testing.assert_array_equal(
                scipy_optimize_module_mock.optimize.minimize.mock_calls[0].args[1],
                array([1, 1, 1]),
            )

            self.assertEqual(
                scipy_optimize_module_mock.optimize.minimize.mock_calls[0].kwargs[
                    "method"
                ],
                "L-BFGS-B",
            )

    def test_CanOptimizeTHypValue(self):
        """Can optimize t_hyp value"""
        polynomials_mock, numpy_module_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return values of called functions
        scipy_optimize_module_mock.optimize.minimize.return_value = OptimizeResult(
            x=2.0
        )

        numpy_module_mock.mean.return_value = 0

        with patch.dict(
            "sys.modules",
            {
                "scipy": scipy_optimize_module_mock,
                "numpy": numpy_module_mock,
            },
        ):
            from napytau.core.chi import optimize_t_hyp

            doppler_shifted_intensities: ndarray = array([2, 6])
            unshifted_intensities: ndarray = array([6, 10])
            delta_doppler_shifted_intensities: ndarray = array([1, 1])
            delta_unshifted_intensities: ndarray = array([1, 1])
            initial_coefficients: ndarray = array([1, 1, 1])
            distances: ndarray = array([0, 1])
            t_hyp_range: Tuple[float, float] = (-5, 5)
            weight_factor: float = 1.0

            expected_t_hyp: float = 2.0

            actual_t_hyp: float = optimize_t_hyp(
                doppler_shifted_intensities,
                unshifted_intensities,
                delta_doppler_shifted_intensities,
                delta_unshifted_intensities,
                initial_coefficients,
                distances,
                t_hyp_range,
                weight_factor,
            )

            self.assertEqual(actual_t_hyp, expected_t_hyp)

            self.assertEqual(
                len(scipy_optimize_module_mock.optimize.minimize.mock_calls), 1
            )

            self.assertTrue(
                callable(
                    scipy_optimize_module_mock.optimize.minimize.mock_calls[0].args[0]
                ),
                """The first argument to minimize should be a callable function""",
            )

            self.assertEqual(
                scipy_optimize_module_mock.optimize.minimize.mock_calls[0].kwargs["x0"],
                0.0,
            )

            self.assertEqual(
                scipy_optimize_module_mock.optimize.minimize.mock_calls[0].kwargs[
                    "bounds"
                ],
                [(t_hyp_range[0], t_hyp_range[1])],
            )

            self.assertEqual(len(numpy_module_mock.mean.mock_calls), 1)

            self.assertEqual(numpy_module_mock.mean.mock_calls[0].args[0], (-5, 5))
