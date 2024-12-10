from __future__ import annotations
from typing import Dict, List, Callable, Iterator

from napytau.ingest.model.datapoint import Datapoint
from napytau.util.coalesce import coalesce
from napytau.util.model.value_error_pair import ValueErrorPair


class DatapointCollection:
    """
    A class to represent a collection of datapoints.
    It provides convenience methods to filter, add, and retrieve datapoints.
    Internally, it uses a dictionary to store the datapoints. The key is the hash
    of the distance value of a given datapoint.

    This class can be iterated over, and it provides a way to access the elements
    """

    elements: Dict[int, Datapoint]

    def __init__(self, raw_datapoints: List[Datapoint]):
        self.elements = {}
        for datapoint in raw_datapoints:
            self.elements[hash(datapoint.distance.value)] = datapoint

    def __len__(self) -> int:
        return len(self.elements)

    def __iter__(self) -> Iterator[Datapoint]:
        return iter(self.elements.values())

    def __getitem__(self, key: int) -> Datapoint:
        return list(self.elements.values())[key]

    def as_dict(self) -> Dict[int, Datapoint]:
        """Return the collection as a dictionary. Keys are the hash of the distance value."""  # noqa E501
        return self.elements

    def filter(self, filter_func: Callable[[Datapoint], bool]) -> DatapointCollection:
        return DatapointCollection(list(filter(filter_func, self.elements.values())))

    def add_datapoint(self, datapoint: Datapoint) -> None:
        self.elements[hash(datapoint.distance.value)] = datapoint

    def get_datapoint_by_distance(self, distance: float) -> Datapoint:
        """
        Get a datapoint by its distance.
        This function will raise an error if the datapoint is not found.
        """
        if hash(distance) not in self.elements:
            raise ValueError(f'Datapoint with distance: "{distance}" not found.')

        return self.elements[hash(distance)]

    def get_distances(self) -> List[ValueErrorPair[float]]:
        return list(
            map(
                lambda datapoint: datapoint.distance,
                self.elements.values(),
            )
        )

    def get_calibrations(self) -> List[ValueErrorPair[float]]:
        return list(
            map(
                lambda datapoint: coalesce(datapoint.calibration),
                self.filter(
                    lambda datapoint: datapoint.calibration is not None
                ).elements.values(),
            )
        )

    def get_shifted_intensities(self) -> List[ValueErrorPair[float]]:
        return list(
            map(
                lambda datapoint: coalesce(datapoint.shifted_intensity),
                self.filter(
                    lambda datapoint: datapoint.shifted_intensity is not None
                ).elements.values(),
            )
        )

    def get_unshifted_intensities(self) -> List[ValueErrorPair[float]]:
        return list(
            map(
                lambda datapoint: coalesce(datapoint.unshifted_intensity),
                self.filter(
                    lambda datapoint: datapoint.unshifted_intensity is not None
                ).elements.values(),
            )
        )

    def get_feeding_shifted_intensities(self) -> List[ValueErrorPair[float]]:
        return list(
            map(
                lambda datapoint: coalesce(datapoint.feeding_shifted_intensity),
                self.filter(
                    lambda datapoint: datapoint.feeding_shifted_intensity is not None
                ).elements.values(),
            )
        )

    def get_feeding_unshifted_intensities(self) -> List[ValueErrorPair[float]]:
        return list(
            map(
                lambda datapoint: coalesce(datapoint.feeding_unshifted_intensity),
                self.filter(
                    lambda datapoint: datapoint.feeding_unshifted_intensity is not None
                ).elements.values(),
            )
        )
