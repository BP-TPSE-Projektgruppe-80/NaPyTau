import customtkinter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.


class CheckboxPanel:
    def __init__(self, parent: "App") -> None:
        """
        Initializes the checkbox panel for the datapoints.
        :param parent: Parent widget to host the checkbox panel.
        """
        self.parent = parent
        self.frame_datapoint_checkboxes = customtkinter.CTkScrollableFrame(
            self.parent, width=200, height=250
        )
        self.frame_datapoint_checkboxes.grid(
            row=0, column=1, padx=0, pady=0, sticky="nsew"
        )

    def update_data_checkboxes_fitting(self) -> None:
        """
        Updates the checkboxes with the current set data points
        for the fitting.
        """
        # Clear all checkboxes for the fitting
        for widget in self.frame_datapoint_checkboxes.winfo_children():
            if widget.grid_info().get("column") == 0:  # Column 0 for fitting
                widget.grid_forget()

        header_label = customtkinter.CTkLabel(
            self.frame_datapoint_checkboxes,
            text="Datapoints for fitting",
            font=("Arial", 16),
        )
        header_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Update all checkboxes for the fitting
        for i in range(len(self.parent.datapoints)):
            x, y = self.parent.datapoints[i]

            checkbox = customtkinter.CTkCheckBox(
                self.frame_datapoint_checkboxes,
                text=f"({x} | {y})",
                variable=customtkinter.IntVar(value=1),
                command=lambda index=i: self._data_checkbox_fitting_event(index),
            )
            checkbox.grid(row=i + 1, column=0, padx=10, pady=2, sticky="nsew")

    def _data_checkbox_fitting_event(self, index: int) -> None:
        """
        Do not call from outside. Is called if a data checkbox
        for the fitting is called.
        Toggles the intern boolean value of the datapoint.
        :param index: Index of the pressed data checkbox.
        """
        self.parent.datapoints_for_fitting[
            index
        ].is_checked = not self.parent.datapoints_for_fitting[index].is_checked
        if self.parent.datapoints_for_fitting[index].is_checked:
            print("[fitting] checkbox with index " + str(index) + " activated.")
        else:
            print("[fitting] checkbox with index " + str(index) + " deactivated.")

    def update_data_checkboxes_calculation(self) -> None:
        """
        Updates the checkboxes with the current set data points for
        the calculation of tau and delta-tau.
        """
        # Clear all checkboxes for the calculation
        for widget in self.frame_datapoint_checkboxes.winfo_children():
            if widget.grid_info().get("column") == 1:
                widget.grid_forget()

        header_label = customtkinter.CTkLabel(
            self.frame_datapoint_checkboxes,
            text="Tau calculation",
            font=("Arial", 16),
        )
        header_label.grid(row=0, column=1, padx=30, pady=5, sticky="nsew")

        # Update all checkboxes for the calculation
        for i in range(len(self.parent.datapoints)):
            x, y = self.parent.datapoints[i]

            checkbox = customtkinter.CTkCheckBox(
                self.frame_datapoint_checkboxes,
                text=f"({x} | {y})",
                variable=customtkinter.IntVar(value=1),
                command=lambda index=i: self._data_checkbox_calculation_event(index),
            )
            checkbox.grid(row=i + 1, column=1, padx=35, pady=2, sticky="nsew")

    def _data_checkbox_calculation_event(self, index: int) -> None:
        """
        Do not call from outside. Is called if a data checkbox for the calculation
        of tau and delta-tau is called.
        Toggles the intern boolean value of the datapoint.
        :param index: Index of the pressed data checkbox.
        """
        self.parent.datapoints_for_calculation[
            index
        ].is_checked = not self.parent.datapoints_for_calculation[index].is_checked
        if self.parent.datapoints_for_calculation[index].is_checked:
            print("[calculation] checkbox with index " + str(index) + " activated.")
        else:
            print("[calculation] checkbox with index " + str(index) + " deactivated.")
