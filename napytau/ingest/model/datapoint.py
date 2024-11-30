from typing import Optional, Tuple

from napytau.util.model.value_error_pair import ValueErrorPair


class Datapoint:
    """
    A class to represent a single datapoint in a dataset.
    Distance acts as a key, identifying the datapoint, therefore it is required.
    All other attributes are optional and can be set later.
    """

    distance: ValueErrorPair[float]
    calibration: Optional[ValueErrorPair[float]]
    shifted_intensity: Optional[ValueErrorPair[float]]
    unshifted_intensity: Optional[ValueErrorPair[float]]
    feeding_shifted_intensity: Optional[ValueErrorPair[float]]
    feeding_unshifted_intensity: Optional[ValueErrorPair[float]]

    def __init__(
        self,
        distance: ValueErrorPair[float],
        calibration: Optional[ValueErrorPair[float]] = None,
        shifted_intensity: Optional[ValueErrorPair[float]] = None,
        unshifted_intensity: Optional[ValueErrorPair[float]] = None,
        feeding_shifted_intensity: Optional[ValueErrorPair[float]] = None,
        feeding_unshifted_intensity: Optional[ValueErrorPair[float]] = None,
    ) -> None:
        self.distance = distance
        self.calibration = calibration
        self.shifted_intensity = shifted_intensity
        self.unshifted_intensity = unshifted_intensity
        self.feeding_shifted_intensity = feeding_shifted_intensity
        self.feeding_unshifted_intensity = feeding_unshifted_intensity

    def get_distance(self) -> ValueErrorPair[float]:
        return self.distance

    def set_distance(self, distance: ValueErrorPair[float]) -> None:
        self.distance = distance

    def get_calibration(self) -> Optional[ValueErrorPair[float]]:
        return self.calibration

    def set_calibration(self, calibration: ValueErrorPair[float]) -> None:
        self.calibration = calibration

    def get_intensity(
        self,
    ) -> Tuple[Optional[ValueErrorPair[float]], Optional[ValueErrorPair[float]]]:
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
