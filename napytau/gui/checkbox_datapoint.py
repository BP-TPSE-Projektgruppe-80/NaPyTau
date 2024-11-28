class CheckboxDataPoint():
    def __init__(self, coordinates: tuple[float, float], is_checked: bool):
        """
        Constructor for the CheckboxDataPoint class.

        :param coordinates: Tuple of the coordinates.
        :param is_checked: Boolean value if the checkbox is checked.
        """
        if not isinstance(coordinates, tuple) or len(coordinates) != 2:
            raise ValueError("coordinates must be a tuple of two float values")
        if not all(isinstance(coord, float) for coord in coordinates):
            raise TypeError("all coordinates must be floats.")
        if not isinstance(is_checked, bool):
            raise TypeError("is_checked must be a bool.")

        self.coordinates = coordinates
        self.is_checked = is_checked

    def toggle_checkbox(self):
        """Toggles the boolean value"""
        self.is_checked = not self.is_checked
