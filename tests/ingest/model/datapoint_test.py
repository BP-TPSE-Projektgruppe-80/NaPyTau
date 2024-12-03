import unittest
from napytau.ingest.model.datapoint import Datapoint
from napytau.util.model.value_error_pair import ValueErrorPair


class DatapointUnitTest(unittest.TestCase):
    def test_raisesAnExceptionIfCalibrationIsAccessedBeforeInitialization(self):
        """Raise an exception if calibration is accessed before initialization."""
        datapoint = Datapoint(ValueErrorPair(1.0, 0.1))
        with self.assertRaises(Exception):
            datapoint.get_calibration()

    def test_raisesAnExceptionIfIntensityIsAccessedBeforeInitialization(self):
        """Raise an exception if intensity is accessed before initialization."""
        datapoint = Datapoint(ValueErrorPair(1.0, 0.1))
        with self.assertRaises(Exception):
            datapoint.get_intensity()


if __name__ == "__main__":
    unittest.main()
