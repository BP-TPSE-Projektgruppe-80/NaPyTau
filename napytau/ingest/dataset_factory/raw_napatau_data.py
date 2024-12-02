from typing import List


class RawNapatauData:
    velocity_rows: List[str]
    distance_rows: List[str]
    fit_rows: List[str]
    calibration_rows: List[str]

    def __init__(
        self,
        velocity_rows: List[str],
        distance_rows: List[str],
        fit_rows: List[str],
        calibration_rows: List[str],
    ):
        self.velocity_rows = velocity_rows
        self.distance_rows = distance_rows
        self.fit_rows = fit_rows
        self.calibration_rows = calibration_rows
