from dataclasses import dataclass

from napytau.ingest.model.datapoint_collection import DatapointCollection
from napytau.ingest.model.relative_velocity import RelativeVelocity


@dataclass
class DataSet:
    """
    A class to represent a dataset.
    A dataset represents the entirety of the data collected from a single observation.
    """

    def get_relative_velocity(self) -> RelativeVelocity:
        return self.relative_velocity

    def get_datapoints(self) -> DatapointCollection:
        return self.datapoints
