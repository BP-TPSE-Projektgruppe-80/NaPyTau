from typing import Optional


class Datapoint:
    """
    A class to represent a single datapoint in a dataset.
    Distance acts as a key, identifying the datapoint, therefore it is required.
    All other attributes are optional and can be set later.
    """

    distance: float
    distance_error: Optional[float]
    calibration: Optional[float]
    calibration_error: Optional[float]
    shifted_intensity: Optional[float]
    shifted_intensity_error: Optional[float]
    unshifted_intensity: Optional[float]
    unshifted_intensity_error: Optional[float]
    feeding_shifted_intensity: Optional[float]
    feeding_shifted_intensity_error: Optional[float]
    feeding_unshifted_intensity: Optional[float]
    feeding_unshifted_intensity_error: Optional[float]

    def __init(
        self,
        distance: float,
        distance_error: Optional[float] = None,
        calibration: Optional[float] = None,
        calibration_error: Optional[float] = None,
        shifted_intensity: Optional[float] = None,
        shifted_intensity_error: Optional[float] = None,
        unshifted_intensity: Optional[float] = None,
        unshifted_intensity_error: Optional[float] = None,
        feeding_shifted_intensity: Optional[float] = None,
        feeding_shifted_intensity_error: Optional[float] = None,
        feeding_unshifted_intensity: Optional[float] = None,
        feeding_unshifted_intensity_error: Optional[float] = None,
    ):
        self.distance = distance
        self.distance_error = distance_error
        self.calibration = calibration
        self.calibration_error = calibration_error
        self.shifted_intensity = shifted_intensity
        self.shifted_intensity_error = shifted_intensity_error
        self.unshifted_intensity = unshifted_intensity
        self.unshifted_intensity_error = unshifted_intensity_error
        self.feeding_shifted_intensity = feeding_shifted_intensity
        self.feeding_shifted_intensity_error = feeding_shifted_intensity_error
        self.feeding_unshifted_intensity = feeding_unshifted_intensity
        self.feeding_unshifted_intensity_error = feeding_unshifted_intensity_error

    def get_distance_information(self) -> [Optional[float], Optional[float]]:
        return self.distance, self.distance_error

    def set_distance_information(self, distance: float, distance_error: float):
        self.distance = distance
        self.distance_error = distance_error

    def get_calibration_information(self) -> [Optional[float], Optional[float]]:
        return self.calibration, self.calibration_error

    def set_calibration_information(self, calibration: float, calibration_error: float):
        self.calibration = calibration
        self.calibration_error = calibration_error

    def get_intensity_information(
        self,
    ) -> [Optional[float], Optional[float], Optional[float], Optional[float]]:
        return (
            self.shifted_intensity,
            self.shifted_intensity_error,
            self.unshifted_intensity,
            self.unshifted_intensity_error,
        )

    def set_intensity_information(
        self,
        shifted_intensity: float,
        shifted_intensity_error: float,
        unshifted_intensity: float,
        unshifted_intensity_error: float,
    ):
        self.shifted_intensity = shifted_intensity
        self.shifted_intensity_error = shifted_intensity_error
        self.unshifted_intensity = unshifted_intensity
        self.unshifted_intensity_error = unshifted_intensity_error

    def get_feeding_intensity_information(
        self,
    ) -> [Optional[float], Optional[float], Optional[float], Optional[float]]:
        return (
            self.feeding_shifted_intensity,
            self.feeding_shifted_intensity_error,
            self.feeding_unshifted_intensity,
            self.feeding_unshifted_intensity_error,
        )

    def set_feeding_intensity_information(
        self,
        feeding_shifted_intensity: float,
        feeding_shifted_intensity_error: float,
        feeding_unshifted_intensity: float,
        feeding_unshifted_intensity_error: float,
    ):
        self.feeding_shifted_intensity = feeding_shifted_intensity
        self.feeding_shifted_intensity_error = feeding_shifted_intensity_error
        self.feeding_unshifted_intensity = feeding_unshifted_intensity
        self.feeding_unshifted_intensity_error = feeding_unshifted_intensity_error
