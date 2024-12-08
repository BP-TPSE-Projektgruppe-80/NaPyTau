import unittest

from napytau.import_export.crawler.napatau_setup_files import NapatauSetupFiles


class NapatauSetupFilesUnitTest(unittest.TestCase):
    def test_raisesAnErrorIfAnyFileIsNotProvided(self):
        """Raises an error if any file is not provided."""
        with self.assertRaises(ValueError):
            NapatauSetupFiles.create_from_file_names([])
        with self.assertRaises(ValueError):
            NapatauSetupFiles.create_from_file_names(
                [
                    "v_c",
                    "test.fit",
                    "norm.fac",
                ]
            )
        with self.assertRaises(ValueError):
            NapatauSetupFiles.create_from_file_names(
                [
                    "distances.dat",
                    "test.fit",
                    "norm.fac",
                ]
            )
        with self.assertRaises(ValueError):
            NapatauSetupFiles.create_from_file_names(
                [
                    "distances.dat",
                    "v_c",
                    "norm.fac",
                ]
            )
        with self.assertRaises(ValueError):
            NapatauSetupFiles.create_from_file_names(
                [
                    "distances.dat",
                    "v_c",
                    "test.fit",
                ]
            )

    def test_canBeCreatedFromAListOfFileNames(self):
        """Can be created from a list of file names."""
        file_names = [
            "distances.dat",
            "v_c",
            "test.fit",
            "norm.fac",
        ]
        setup_files = NapatauSetupFiles.create_from_file_names(file_names)
        self.assertEqual(setup_files.distances_file, "distances.dat")
        self.assertEqual(setup_files.velocity_file, "v_c")
        self.assertEqual(setup_files.fit_file, "test.fit")
        self.assertEqual(setup_files.calibration_file, "norm.fac")


if __name__ == "__main__":
    unittest.main()
