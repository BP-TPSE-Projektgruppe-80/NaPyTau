import unittest

from napytau.ingest.dataset_factory.napatau_dataset_factory import NapatauDatasetFactory
from napytau.ingest.dataset_factory.raw_napatau_data import RawNapatauData


class NapatauDatasetFactoryUnitTest(unittest.TestCase):
    def test_raisesAnExceptionIfNoVelocityIsProvided(self):
        """Raises an exception if no velocity is provided"""
        with self.assertRaises(ValueError):
            NapatauDatasetFactory.create_dataset(
                RawNapatauData(
                    [],
                    [],
                    [],
                    [],
                )
            )

    def test_raisesAnExceptionIfAnInvalidDistanceRowIsProvided(self):
        """Raises an exception if an invalid distance row is provided"""
        with self.assertRaises(ValueError):
            NapatauDatasetFactory.create_dataset(
                RawNapatauData(
                    ["1"],
                    ["invalid"],
                    ["1 1 1 1 1"],
                    ["1 1 1"],
                )
            )

    def test_raisesAnExceptionIfAnInvalidCalibrationRowIsProvided(self):
        """Raises an exception if an invalid calibration row is provided"""
        with self.assertRaises(ValueError):
            NapatauDatasetFactory.create_dataset(
                RawNapatauData(
                    ["1"],
                    ["1 1 1"],
                    ["1 1 1 1 1"],
                    ["invalid"],
                )
            )

    def test_raisesAnExceptionIfAnInvalidFitRowIsProvided(self):
        """Raises an exception if an invalid fit row is provided"""
        with self.assertRaises(ValueError):
            NapatauDatasetFactory.create_dataset(
                RawNapatauData(
                    ["1"],
                    ["1 1 1"],
                    ["invalid"],
                    ["1 1 1"],
                )
            )

    def test_createsADatasetFromValidDataWithoutFeedingIntensities(self):
        """Creates a dataset from valid data"""
        dataset = NapatauDatasetFactory.create_dataset(
            RawNapatauData(
                ["1"],
                ["1 1 1"],
                ["1 1 1 1 1"],
                ["1 1 1"],
            )
        )

        self.assertEqual(dataset.relative_velocity.get_velocity(), 1)
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
        dataset = NapatauDatasetFactory.create_dataset(
            RawNapatauData(
                ["1"],
                ["1 1 1"],
                ["1 1 1 1 1 1 1 1 1"],
                ["1 1 1"],
            )
        )

        self.assertEqual(dataset.relative_velocity.get_velocity(), 1)
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


if __name__ == "__main__":
    unittest.main()
