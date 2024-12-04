class CheckboxDataPoint:
    def __init__(self, coordinates: tuple[float, float], is_checked: bool):
        """
        Constructor for the CheckboxDataPoint class.

        :param coordinates: The coordinates of the data point.
        :param is_checked: Value if the checkbox is ticked or not.
        """

        self.coordinates = coordinates
        self.is_checked = is_checked

    def toggle_state(self) -> None:
        """
        This method toggles the internal state of the datapoint.
        """
        self.is_checked = not self.is_checked
