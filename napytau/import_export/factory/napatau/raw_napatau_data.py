from dataclasses import dataclass
from typing import List

@dataclass
class RawNapatauData:
    velocity_rows: List[str]
    distance_rows: List[str]
    fit_rows: List[str]
    calibration_rows: List[str]
