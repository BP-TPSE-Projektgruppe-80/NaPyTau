import unittest

from napytau.import_export.factory.napatau.napatau_factory import (
    NapatauFactory,
)
from napytau.import_export.factory.napatau.raw_napatau_data import RawNapatauData


class NapatauFactoryUnitTest(unittest.TestCase):
    def test_raisesAnExceptionIfNoVelocityIsProvided(self):
        """Raises an exception if no velocity is provided"""
        with self.assertRaises(ValueError):
            NapatauFactory.create_dataset(
                RawNapatauData(
                    [],
                    [],
                    [],
                    [],
                )
            )

    def test_raisesAnExceptionIfADistanceRowWithTooFewValuesIsProvided(self):
        """Raises an exception if a distance row with too few values is provided"""
        with self.assertRaises(ValueError):
            NapatauFactory.create_dataset(
                RawNapatauData(
                    ["1"],
                    ["1"],
                    ["1 1 1 1 1"],
                    ["1 1 1"],
                )
            )

    def test_raisesAnExceptionIfADistanceRowWithTooManyValuesIsProvided(self):
        """Raises an exception if a distance row with too many values is provided"""
        with self.assertRaises(ValueError):
            NapatauFactory.create_dataset(
                RawNapatauData(
                    ["1"],
                    ["1 1 1 1"],
                    ["1 1 1 1 1"],
                    ["1 1 1"],
                )
            )

    def test_raisesAnExceptionIfACalibrationRowWithTooFewValuesIsProvided(self):
        """Raises an exception if a calibration row with too few values is provided"""
        with self.assertRaises(ValueError):
            NapatauFactory.create_dataset(
                RawNapatauData(
                    ["1"],
                    ["1 1 1"],
                    ["1 1 1 1 1"],
                    ["1 1"],
                )
            )

    def test_raisesAnExceptionIfACalibrationRowWithTooManyValuesIsProvided(self):
        """Raises an exception if a calibration row with too many values is provided"""
        with self.assertRaises(ValueError):
            NapatauFactory.create_dataset(
                RawNapatauData(
                    ["1"],
                    ["1 1 1"],
                    ["1 1 1 1 1"],
                    ["1 1 1 1"],
                )
            )

    def test_raisesAnExceptionIfAFitRowWithTooFewValuesIsProvided(self):
        """Raises an exception if a fit row with too few values is provided"""
        with self.assertRaises(ValueError):
            NapatauFactory.create_dataset(
                RawNapatauData(
                    ["1"],
                    ["1 1 1"],
                    ["1 1 1 1 1"],
                    ["1 1"],
                )
            )

    def test_raisesAnExceptionIfAFitRowWithTooManyValuesForASetOfBasicIntensitiesButTooManyForASetOfBasicAndShiftedIntensitiesIsProvided(  # noqa: E501
        self,
    ):
        """Raises an exception if a fit row with too many values for a set of basic intensities but too many for a set of basic and shifted intensities is provided"""  # noqa: E501
        with self.assertRaises(ValueError):
            NapatauFactory.create_dataset(
                RawNapatauData(
                    ["1"],
                    ["1 1 1"],
                    ["1 1 1 1 1 1 1 1"],
                    ["1 1 1"],
                )
            )

    def test_raisesAnExceptionIfAFitRowWithTooManyValuesIsProvided(self):
        """Raises an exception if a fit row with too many values is provided"""
        with self.assertRaises(ValueError):
            NapatauFactory.create_dataset(
                RawNapatauData(
                    ["1"],
                    ["1 1 1"],
                    ["1 1 1 1 1 1 1 1 1 1"],
                    ["1 1 1"],
                )
            )

    def test_createsADatasetFromValidDataWithoutFeedingIntensities(self):
        """Creates a dataset from valid data"""
        dataset = NapatauFactory.create_dataset(
            RawNapatauData(
                ["1"],
                ["1 1 1"],
                ["1 1 1 1 1"],
                ["1 1 1"],
            )
        )

        self.assertEqual(dataset.relative_velocity.value.get_velocity(), 1)
        self.assertEqual(dataset.relative_velocity.error.get_velocity(), 0)
        self.assertEqual(len(dataset.datapoints.as_dict()), 1)
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).distance.value, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).distance.error, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).calibration.value, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).calibration.error, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).shifted_intensity.value, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).shifted_intensity.error, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).unshifted_intensity.value, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).unshifted_intensity.error, 1
        )

    def test_createsADatasetFromValidDataWithFeedingIntensities(self):
        """Creates a dataset from valid data with feeding intensities"""
        dataset = NapatauFactory.create_dataset(
            RawNapatauData(
                ["1"],
                ["1 1 1"],
                ["1 1 1 1 1 1 1 1 1"],
                ["1 1 1"],
            )
        )

        self.assertEqual(dataset.relative_velocity.value.get_velocity(), 1)
        self.assertEqual(dataset.relative_velocity.error.get_velocity(), 0)
        self.assertEqual(len(dataset.datapoints.as_dict()), 1)
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).distance.value, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).distance.error, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).calibration.value, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).calibration.error, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).shifted_intensity.value, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).shifted_intensity.error, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).unshifted_intensity.value, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(1).unshifted_intensity.error, 1
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(
                1
            ).feeding_shifted_intensity.value,
            1,
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(
                1
            ).feeding_shifted_intensity.error,
            1,
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(
                1
            ).feeding_unshifted_intensity.value,
            1,
        )
        self.assertEqual(
            dataset.datapoints.get_datapoint_by_distance(
                1
            ).feeding_unshifted_intensity.error,
            1,
        )

    def test_createsADatasetFromValidDataWithAVelocityErrorGiven(self):
        """Creates a dataset from valid data with a velocity error given"""
        dataset = NapatauFactory.create_dataset(
            RawNapatauData(
                ["1 1"],
                ["1 1 1"],
                ["1 1 1 1 1"],
                ["1 1 1"],
            )
        )

        self.assertEqual(dataset.relative_velocity.value.get_velocity(), 1)
        self.assertEqual(dataset.relative_velocity.error.get_velocity(), 1)
        self.assertEqual(len(dataset.datapoints.as_dict()), 1)


if __name__ == "__main__":
    unittest.main()
