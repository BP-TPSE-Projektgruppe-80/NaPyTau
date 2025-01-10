from napytau.import_export.model.datapoint import Datapoint


class CheckboxDataPoint:
    def __init__(self, data: Datapoint, is_checked: bool):
        """
        Constructor for the CheckboxDataPoint class.

        :param coordinates: The coordinates of the data point.
        :param is_checked: Value if the checkbox is ticked or not.
        """

        self.data = data
        self.is_checked = is_checked

    def toggle_state(self) -> None:
        """
        This method toggles the internal state of the datapoint.
        """
        self.is_checked = not self.is_checked

    def get_distance_value(self) -> float:
        return self.data.get_distance().value

    def get_shifted_intensity_value(self) -> float:
        return self.data.get_intensity()[0].value

    def get_shifted_intensity_error(self) -> float:
        return self.data.get_intensity()[0].error



def get_checked_datapoints( datapoints: list[CheckboxDataPoint]) -> list[CheckboxDataPoint]:

    checked_datapoints: list[CheckboxDataPoint] = []
    for datapoint in datapoints:
        if datapoint.is_checked:
            checked_datapoints.append(datapoint)

    return checked_datapoints



def get_distances( datapoints: list[CheckboxDataPoint]) -> list[float]:

    distances = []
    for datapoint in datapoints:
        distances.append(datapoint.get_distance_value())

    return distances

def get_shifted_intensities( datapoints: list[CheckboxDataPoint]) -> list[float]:

    intensities = []
    for datapoint in datapoints:
        intensities.append(datapoint.get_shifted_intensity_value())

    return intensities

