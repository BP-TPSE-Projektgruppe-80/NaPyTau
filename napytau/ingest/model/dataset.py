from napytau.ingest.model.datapoint_collection import DatapointCollection
from napytau.ingest.model.relative_velocity import RelativeVelocity


class DataSet:
    def __init__(
        self, relative_velocity: RelativeVelocity, datapoints: DatapointCollection
    ):
        self.relative_velocity = relative_velocity
        self.datapoints = datapoints
