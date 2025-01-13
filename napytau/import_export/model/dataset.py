from dataclasses import dataclass
from typing import Optional, List

from napytau.import_export.model.datapoint_collection import DatapointCollection
from napytau.import_export.model.polynomial import Polynomial
from napytau.import_export.model.relative_velocity import RelativeVelocity
from napytau.util.model.value_error_pair import ValueErrorPair


@dataclass
class DataSet:
    """
    A class to represent a dataset.
    A dataset represents the entirety of the data collected from a single observation.
    """

    relative_velocity: ValueErrorPair[RelativeVelocity]
    datapoints: DatapointCollection
    tau_factor: Optional[float] = None
    weighted_mean_tau: Optional[ValueErrorPair[float]] = None
    sampling_points: Optional[List[float]] = None
    polynomial_count: Optional[int] = None
    polynomials: Optional[List[Polynomial]] = None

    def get_relative_velocity(self) -> ValueErrorPair[RelativeVelocity]:
        return self.relative_velocity

    def get_datapoints(self) -> DatapointCollection:
        return self.datapoints

    def get_tau_factor(self) -> Optional[float]:
        return self.tau_factor

    def set_tau_factor(self, tau_factor: float) -> None:
        self.tau_factor = tau_factor

    def get_weighted_mean_tau(self) -> Optional[ValueErrorPair[float]]:
        return self.weighted_mean_tau

    def set_weighted_mean_tau(self, weighted_mean_tau: ValueErrorPair[float]) -> None:
        self.weighted_mean_tau = weighted_mean_tau

    def get_sampling_points(self) -> Optional[List[float]]:
        return self.sampling_points

    def set_sampling_points(self, sampling_points: List[float]) -> None:
        self.sampling_points = sampling_points

    def get_polynomial_count(self) -> Optional[int]:
        return self.polynomial_count

    def set_polynomial_count(self, polynomial_count: int) -> None:
        self.polynomial_count = polynomial_count

    def get_polynomials(self) -> Optional[List[Polynomial]]:
        return self.polynomials

    def set_polynomials(self, polynomials: List[Polynomial]) -> None:
        self.polynomials = polynomials
