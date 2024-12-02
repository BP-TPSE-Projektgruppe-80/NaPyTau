from __future__ import annotations

from typing import List


class NapatauSetupFiles:
    distances_file: str
    velocity_file: str
    fit_file: str
    calibration_file: str

    def __init__(
        self,
        distances_file: str,
        velocity_file: str,
        fit_file: str,
        calibration_file: str,
    ):
        """Use the static constructor method instead"""
        self.distances_file = distances_file
        self.velocity_file = velocity_file
        self.fit_file = fit_file
        self.calibration_file = calibration_file

    @staticmethod
    def create_from_file_names(file_names: List[str]) -> NapatauSetupFiles:
        try:
            distances_file = next(
                file for file in file_names if "distances.dat" in file
            )
            velocity_file = next(file for file in file_names if "v_c" in file)
            fit_file = next(file for file in file_names if "fit" in file)
            calibration_file = next(file for file in file_names if "norm.fac" in file)
        except StopIteration:
            raise ValueError(
                "Could not find all necessary files in the provided list of file names."
            )

        return NapatauSetupFiles(
            distances_file, velocity_file, fit_file, calibration_file
        )
