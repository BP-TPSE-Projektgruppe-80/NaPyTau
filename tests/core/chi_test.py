import unittest
from unittest.mock import MagicMock, patch
from numpy import array
from numpy import ndarray
from numpy import testing
from numpy import mean
from scipy.optimize import OptimizeResult

def set_up_mocks() -> (MagicMock, MagicMock):
    polynomials_mock = MagicMock()
    polynomials_mock.polynomial_sum_at_measuring_times = MagicMock()
    polynomials_mock.differentiated_polynomial_sum_at_measuring_times = MagicMock()

    scipy_optimize_module_mock = MagicMock()
    scipy_optimize_module_mock.minimize = MagicMock()
    return polynomials_mock, scipy_optimize_module_mock


class ChiUnitTests(unittest.TestCase):
    def test_ChiCalculationForValidData(self):
        polynomials_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return values of called functions
        polynomials_mock.polynomial_sum_at_measuring_times\
            .return_value = array([5, 15, 57])
        polynomials_mock.differentiated_polynomial_sum_at_measuring_times\
            .return_value = array([4, 20, 72])


        with patch.dict(
                "sys.modules",
                {
                    "napytau.core.polynomials": polynomials_mock,
                },
            ):

            from napytau.core.chi import chi_squared_fixed_t

            # Mocked input data
            doppler_shifted_intensities: ndarray = array([1, 2, 3])
            unshifted_intensities: ndarray = array([4, 5, 6])
            delta_doppler_shifted_intensities: ndarray = array([2, 3, 4])
            delta_unshifted_intensities: ndarray = array([5, 6, 7])
            coefficients: ndarray = array([5, 4, 3, 2, 1])
            times: ndarray = array([0, 1, 2])
            t_hyp: float = 2.0
            weight_factor: float = 1.0

            # Expected result
            expected_result: float = 628.3486168


            self.assertAlmostEqual(
                chi_squared_fixed_t(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    coefficients,
                    times,
                    t_hyp,
                    weight_factor,
                ),
                expected_result,
            )


            self.assertEqual(
                len(polynomials_mock.polynomial_sum_at_measuring_times.mock_calls), 1
            )

            testing.assert_array_equal(
                polynomials_mock.polynomial_sum_at_measuring_times.mock_calls[0].args[0],
                (array([0, 1, 2])),
            )

            testing.assert_array_equal(
                polynomials_mock.polynomial_sum_at_measuring_times.mock_calls[0].args[
                    1],
                (array([5, 4, 3, 2, 1])),
            )


            self.assertEqual(
                len(
                    polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                    .mock_calls
                ),
                1,
            )

            testing.assert_array_equal(
                polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                .mock_calls[0].args[0],
                (array([0, 1, 2])),
            )

            testing.assert_array_equal(
                polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                .mock_calls[0].args[1],
                (array([5, 4, 3, 2, 1])),
            )


    def test_ChiCalculationForEmptyDataArrays(self):
        polynomials_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return values of called functions
        polynomials_mock.polynomial_sum_at_measuring_times\
            .return_value = array([])
        polynomials_mock.differentiated_polynomial_sum_at_measuring_times\
            .return_value = array([])


        with patch.dict(
                "sys.modules",
                {
                    "napytau.core.polynomials": polynomials_mock,
                },
        ):

            from napytau.core.chi import chi_squared_fixed_t

            # Mocked input data
            doppler_shifted_intensities: ndarray = array([])
            unshifted_intensities: ndarray = array([])
            delta_doppler_shifted_intensities: ndarray = array([])
            delta_unshifted_intensities: ndarray = array([])
            coefficients: ndarray = array([])
            times: ndarray = array([])
            t_hyp: float = 2.0
            weight_factor: float = 1.0

            # Expected result
            expected_result: float = 0


            self.assertEqual(
                chi_squared_fixed_t(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    coefficients,
                    times,
                    t_hyp,
                    weight_factor,
                ),
                expected_result,
            )


            self.assertEqual(
                len(polynomials_mock.polynomial_sum_at_measuring_times.mock_calls), 1
            )

            testing.assert_array_equal(
                polynomials_mock.polynomial_sum_at_measuring_times.mock_calls[0].args[0],
                (array([])),
            )

            testing.assert_array_equal(
                polynomials_mock.polynomial_sum_at_measuring_times.mock_calls[0].args[
                    1],
                (array([])),
            )


            self.assertEqual(
                len(
                    polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                    .mock_calls
                ),
                1,
            )

            testing.assert_array_equal(
                polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                .mock_calls[0].args[0],
                (array([])),
            )

            testing.assert_array_equal(
                polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                .mock_calls[0].args[1],
                (array([])),
            )


    def test_ChiCalculationForSingleDatapoint(self):
        polynomials_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return values of called functions
        polynomials_mock.polynomial_sum_at_measuring_times\
            .return_value = array([57])
        polynomials_mock.differentiated_polynomial_sum_at_measuring_times\
            .return_value = array([72])


        with patch.dict(
                "sys.modules",
                {
                    "napytau.core.polynomials": polynomials_mock,
                },
        ):

            from napytau.core.chi import chi_squared_fixed_t

            # Mocked input data
            doppler_shifted_intensities: ndarray = array([1])
            unshifted_intensities: ndarray = array([2])
            delta_doppler_shifted_intensities: ndarray = array([3])
            delta_unshifted_intensities: ndarray = array([4])
            coefficients: ndarray = array([5, 4, 3, 2, 1])
            times: ndarray = array([2])
            t_hyp: float = 2.0
            weight_factor: float = 1.0

            # Expected result
            expected_result: float = 1608.694444444444


            self.assertAlmostEqual(
                chi_squared_fixed_t(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    coefficients,
                    times,
                    t_hyp,
                    weight_factor,
                ),
                expected_result,
            )


            self.assertEqual(
                len(polynomials_mock.polynomial_sum_at_measuring_times.mock_calls), 1
            )

            testing.assert_array_equal(
                polynomials_mock.polynomial_sum_at_measuring_times.mock_calls[0].args[0],
                (array([2])),
            )

            testing.assert_array_equal(
                polynomials_mock.polynomial_sum_at_measuring_times.mock_calls[0].args[
                    1],
                (array([5, 4, 3, 2, 1])),
            )


            self.assertEqual(
                len(
                    polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                    .mock_calls
                ),
                1,
            )

            testing.assert_array_equal(
                polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                .mock_calls[0].args[0],
                (array([2])),
            )

            testing.assert_array_equal(
                polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                .mock_calls[0].args[1],
                (array([5, 4, 3, 2, 1])),
            )


    def test_ChiCalculationForDenominatorZero(self):
        polynomials_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return values of called functions
        polynomials_mock.polynomial_sum_at_measuring_times\
            .return_value = array([5, 15])
        polynomials_mock.differentiated_polynomial_sum_at_measuring_times\
            .return_value = array([4, 20])


        with patch.dict(
                "sys.modules",
                {
                    "napytau.core.polynomials": polynomials_mock,
                },
        ):

            from napytau.core.chi import chi_squared_fixed_t

            # Mocked input data
            doppler_shifted_intensities: ndarray = array([1, 2])
            unshifted_intensities: ndarray = array([3, 4])
            delta_doppler_shifted_intensities: ndarray = array([0, 1])
            delta_unshifted_intensities: ndarray = array([0, 1])
            coefficients: ndarray = array([5, 4, 3, 2, 1])
            times: ndarray = array([0, 1])
            t_hyp: float = 2.0
            weight_factor: float = 1.0

            # Expected result
            expected_result: float = float('inf')


            self.assertAlmostEqual(
                chi_squared_fixed_t(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    coefficients,
                    times,
                    t_hyp,
                    weight_factor,
                ),
                expected_result,
            )


            self.assertEqual(
                len(polynomials_mock.polynomial_sum_at_measuring_times.mock_calls), 1
            )

            testing.assert_array_equal(
                polynomials_mock.polynomial_sum_at_measuring_times.mock_calls[0].args[0],
                (array([0, 1])),
            )

            testing.assert_array_equal(
                polynomials_mock.polynomial_sum_at_measuring_times.mock_calls[0].args[
                    1],
                (array([5, 4, 3, 2, 1])),
            )


            self.assertEqual(
                len(
                    polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                    .mock_calls
                ),
                1,
            )

            testing.assert_array_equal(
                polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                .mock_calls[0].args[0],
                (array([0, 1])),
            )

            testing.assert_array_equal(
                polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                .mock_calls[0].args[1],
                (array([5, 4, 3, 2, 1])),
            )


    def test_ChiCalculationForNegativeValues(self):
        polynomials_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return values of called functions
        polynomials_mock.polynomial_sum_at_measuring_times\
            .return_value = array([-5, -5])
        polynomials_mock.differentiated_polynomial_sum_at_measuring_times\
            .return_value = array([-4, -4])


        with patch.dict(
                "sys.modules",
                {
                    "napytau.core.polynomials": polynomials_mock,
                },
        ):

            from napytau.core.chi import chi_squared_fixed_t

            # Mocked input data
            doppler_shifted_intensities: ndarray = array([-1, -2])
            unshifted_intensities: ndarray = array([-3, -4])
            delta_doppler_shifted_intensities: ndarray = array([1, 2])
            delta_unshifted_intensities: ndarray = array([3, 4])
            coefficients: ndarray = array([-5, -4, 3, 2, -1])
            times: ndarray = array([0, 1])
            t_hyp: float = 2.0
            weight_factor: float = 1.0

            # Expected result
            expected_result: float = 22.02777778


            self.assertAlmostEqual(
                chi_squared_fixed_t(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    coefficients,
                    times,
                    t_hyp,
                    weight_factor,
                ),
                expected_result,
            )


            self.assertEqual(
                len(polynomials_mock.polynomial_sum_at_measuring_times.mock_calls), 1
            )

            testing.assert_array_equal(
                polynomials_mock.polynomial_sum_at_measuring_times.mock_calls[0].args[0],
                (array([0, 1])),
            )

            testing.assert_array_equal(
                polynomials_mock.polynomial_sum_at_measuring_times.mock_calls[0].args[
                    1],
                (array([-5, -4, 3, 2, -1])),
            )


            self.assertEqual(
                len(
                    polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                    .mock_calls
                ),
                1,
            )

            testing.assert_array_equal(
                polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                .mock_calls[0].args[0],
                (array([0, 1])),
            )

            testing.assert_array_equal(
                polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                .mock_calls[0].args[1],
                (array([-5, -4, 3, 2, -1])),
            )


    def test_ChiCalculationForWeightFactorZero(self):
        polynomials_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return values of called functions
        polynomials_mock.polynomial_sum_at_measuring_times\
            .return_value = array([5, 15, 57])
        polynomials_mock.differentiated_polynomial_sum_at_measuring_times\
            .return_value = array([4, 20, 72])


        with patch.dict(
                "sys.modules",
                {
                    "napytau.core.polynomials": polynomials_mock,
                },
        ):

            from napytau.core.chi import chi_squared_fixed_t

            # Mocked input data
            doppler_shifted_intensities: ndarray = array([1, 2, 3])
            unshifted_intensities: ndarray = array([4, 5, 6])
            delta_doppler_shifted_intensities: ndarray = array([2, 3, 4])
            delta_unshifted_intensities: ndarray = array([5, 6, 7])
            coefficients: ndarray = array([5, 4, 3, 2, 1])
            times: ndarray = array([0, 1, 2])
            t_hyp: float = 2.0
            weight_factor: float = 0.0

            # Expected result
            expected_result: float = 205.0277778


            self.assertAlmostEqual(
                chi_squared_fixed_t(
                    doppler_shifted_intensities,
                    unshifted_intensities,
                    delta_doppler_shifted_intensities,
                    delta_unshifted_intensities,
                    coefficients,
                    times,
                    t_hyp,
                    weight_factor,
                ),
                expected_result,
            )


            self.assertEqual(
                len(polynomials_mock.polynomial_sum_at_measuring_times.mock_calls), 1
            )

            testing.assert_array_equal(
                polynomials_mock.polynomial_sum_at_measuring_times.mock_calls[0].args[0],
                (array([0, 1, 2])),
            )

            testing.assert_array_equal(
                polynomials_mock.polynomial_sum_at_measuring_times.mock_calls[0].args[
                    1],
                (array([5, 4, 3, 2, 1])),
            )


            self.assertEqual(
                len(
                    polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                    .mock_calls
                ),
                1,
            )

            testing.assert_array_equal(
                polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                .mock_calls[0].args[0],
                (array([0, 1, 2])),
            )

            testing.assert_array_equal(
                polynomials_mock.differentiated_polynomial_sum_at_measuring_times
                .mock_calls[0].args[1],
                (array([5, 4, 3, 2, 1])),
            )


    def test_coefficientOptimization(self):
        polynomials_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return value of called function
        scipy_optimize_module_mock.minimize.return_value = OptimizeResult(x = [2, 3, 1],
                                                                          fun = 0.0)


        with patch.dict(
                "sys.modules",
                {
                    "scipy.optimize": scipy_optimize_module_mock,
                },
        ):

            from napytau.core.chi import optimize_coefficients

            # Mocked input data
            doppler_shifted_intensities: ndarray = array([2, 6])
            unshifted_intensities: ndarray = array([6, 10])
            delta_doppler_shifted_intensities: ndarray = array([1, 1])
            delta_unshifted_intensities: ndarray = array([1, 1])
            initial_coefficients: ndarray = array([1, 1, 1])
            times: ndarray = array([0, 1])
            t_hyp: float = 2.0
            weight_factor: float = 1.0

            # Expected result
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
                                                times,
                                                t_hyp,
                                                weight_factor)

            self.assertEqual(actual_chi, expected_chi)
            testing.assert_array_equal(actual_coefficients, expected_coefficients)


            self.assertEqual(
                len(scipy_optimize_module_mock.minimize.mock_calls), 1
            )

            testing.assert_array_equal(
                scipy_optimize_module_mock.minimize.mock_calls[0].args[1],
                array([1, 1, 1]),
            )

            self.assertEqual(
                scipy_optimize_module_mock.minimize.mock_calls[0].kwargs["method"],
                "L-BFGS-B",
            )


    def test_tHypOptimization(self):
        polynomials_mock, scipy_optimize_module_mock = set_up_mocks()

        # Mocked return value of called function
        scipy_optimize_module_mock.minimize.return_value = OptimizeResult(x=2.0)


        with patch.dict(
                "sys.modules",
                {
                    "scipy.optimize": scipy_optimize_module_mock,
                },
        ):

            from napytau.core.chi import optimize_t_hyp

            # Mocked input data
            doppler_shifted_intensities: ndarray = array([2, 6])
            unshifted_intensities: ndarray = array([6, 10])
            delta_doppler_shifted_intensities: ndarray = array([1, 1])
            delta_unshifted_intensities: ndarray = array([1, 1])
            initial_coefficients: ndarray = array([1, 1, 1])
            times: ndarray = array([0, 1])
            t_hyp_range: (float, float) = (-5, 5)
            weight_factor: float = 1.0

            # Expected result
            expected_t_hyp: float = 2.0

            actual_t_hyp: float = optimize_t_hyp(doppler_shifted_intensities,
                                                 unshifted_intensities,
                                                 delta_doppler_shifted_intensities,
                                                 delta_unshifted_intensities,
                                                 initial_coefficients,
                                                 times,
                                                 t_hyp_range,
                                                 weight_factor)

            self.assertEqual(actual_t_hyp, expected_t_hyp)

            self.assertEqual(
                len(scipy_optimize_module_mock.minimize.mock_calls), 1
            )

            self.assertTrue(
                callable(scipy_optimize_module_mock.minimize.mock_calls[0].args[0]),
                """The first argument to minimize should be a callable (objective function)"""
            )

            self.assertEqual(
                scipy_optimize_module_mock.minimize.mock_calls[0].kwargs["x0"],
                mean(t_hyp_range),
            )

            self.assertEqual(
                scipy_optimize_module_mock.minimize.mock_calls[0].kwargs["bounds"],
                [(t_hyp_range[0], t_hyp_range[1])],
            )