from napytau.ingest.model.datapoint_collection import DatapointCollection
from napytau.ingest.model.relative_velocity import RelativeVelocity


class DataSet:
    def __init__(
        self, relative_velocity: RelativeVelocity, datapoints: DatapointCollection
    ):
        self.relative_velocity = relative_velocity
        self.datapoints = datapoints

    def get_relative_velocity(self) -> RelativeVelocity:
        return self.relative_velocity

    def get_datapoints(self) -> DatapointCollection:
        return self.datapoints
