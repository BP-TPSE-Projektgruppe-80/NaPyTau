from dataclasses import dataclass
from typing import Optional, Tuple

from napytau.util.model.value_error_pair import ValueErrorPair


@dataclass
class Datapoint:
    """
    A class to represent a single datapoint in a dataset.
    Distance acts as a key, identifying the datapoint, therefore it is required.
    All other attributes are optional and can be set later.

    As this class sits at the core of the entire system, it is important to take care
    when modifying it. Any changes to this class will have a ripple effect on the entire
    system.
    """

    distance: ValueErrorPair[float]
    calibration: Optional[ValueErrorPair[float]] = None
    shifted_intensity: Optional[ValueErrorPair[float]] = None
    unshifted_intensity: Optional[ValueErrorPair[float]] = None
    feeding_shifted_intensity: Optional[ValueErrorPair[float]] = None
    feeding_unshifted_intensity: Optional[ValueErrorPair[float]] = None

    def get_distance(self) -> ValueErrorPair[float]:
        return self.distance

    def set_distance(self, distance: ValueErrorPair[float]) -> None:
        self.distance = distance

    def get_calibration(self) -> ValueErrorPair[float]:
        if self.calibration is None:
            raise ValueError("Calibration was accessed before initialization.")

        return self.calibration

    def set_calibration(self, calibration: ValueErrorPair[float]) -> None:
        self.calibration = calibration

    def get_intensity(self) -> Tuple[ValueErrorPair[float], ValueErrorPair[float]]:
        if self.shifted_intensity is None or self.unshifted_intensity is None:
            raise ValueError("Intensity was accessed before initialization.")

        return (
            self.shifted_intensity,
            self.unshifted_intensity,
        )

    def set_intensity(
        self,
        shifted_intensity: ValueErrorPair[float],
        unshifted_intensity: ValueErrorPair[float],
    ) -> None:
        self.shifted_intensity = shifted_intensity
        self.unshifted_intensity = unshifted_intensity

    def get_feeding_intensity(
        self,
    ) -> Tuple[Optional[ValueErrorPair[float]], Optional[ValueErrorPair[float]]]:
        return (
            self.feeding_shifted_intensity,
            self.feeding_unshifted_intensity,
        )

    def set_feeding_intensity(
        self,
        feeding_shifted_intensity: ValueErrorPair[float],
        feeding_unshifted_intensity: ValueErrorPair[float],
    ) -> None:
        self.feeding_shifted_intensity = feeding_shifted_intensity
        self.feeding_unshifted_intensity = feeding_unshifted_intensity
