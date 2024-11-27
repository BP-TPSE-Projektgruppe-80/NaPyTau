from typing import Dict, List, Tuple

from napytau.ingest.model.datapoint import Datapoint


class DatapointCollection:
    elements: Dict[float, Datapoint]

    def __init__(self, raw_datapoints: List[Datapoint]):
        self.elements = {}
        for datapoint in raw_datapoints:
            self.elements[datapoint.distance] = datapoint

    def as_list(self) -> Dict[float, Datapoint]:
        return self.elements

    def add_datapoint(self, datapoint: Datapoint):
        self.elements[datapoint.distance] = datapoint

    def get_datapoint_by_distance(self, distance: float) -> Datapoint:
        return self.elements[distance]

    def get_distances(self) -> List[Tuple[float, float]]:
        return list(
            map(
                lambda datapoint: (datapoint.distance, datapoint.distance_error),
                self.elements.values(),
            )
        )

    def get_calibrations(self) -> List[Tuple[float, float]]:
        return list(
            map(
                lambda datapoint: (datapoint.calibration, datapoint.calibration_error),
                self.elements.values(),
            )
        )

    def get_shifted_intensities(self) -> List[Tuple[float, float]]:
        return list(
            map(
                lambda datapoint: (
                    datapoint.shifted_intensity,
                    datapoint.shifted_intensity_error,
                ),
                self.elements.values(),
            )
        )

    def get_unshifted_intensities(self) -> List[Tuple[float, float]]:
        return list(
            map(
                lambda datapoint: (
                    datapoint.unshifted_intensity,
                    datapoint.unshifted_intensity_error,
                ),
                self.elements.values(),
            )
        )

    def get_feeding_shifted_intensities(self) -> List[Tuple[float, float]]:
        return list(
            map(
                lambda datapoint: (
                    datapoint.feeding_shifted_intensity,
                    datapoint.feeding_shifted_intensity_error,
                ),
                self.elements.values(),
            )
        )

    def get_feeding_unshifted_intensities(self) -> List[Tuple[float, float]]:
        return list(
            map(
                lambda datapoint: (
                    datapoint.feeding_unshifted_intensity,
                    datapoint.feeding_unshifted_intensity_error,
                ),
                self.elements.values(),
            )
        )
