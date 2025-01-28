from typing import List

import tkinter as tk
from tkinter import filedialog

import customtkinter

from napytau.cli.cli_arguments import CLIArguments

from napytau.gui.components.checkbox_panel import CheckboxPanel
from napytau.gui.components.control_panel import ControlPanel
from napytau.gui.components.graph import Graph
from napytau.gui.components.logger import Logger, LogMessageType
from napytau.gui.components.menu_bar import MenuBar
from napytau.gui.components.Toolbar import Toolbar

from napytau.import_export.model.datapoint import Datapoint
from napytau.import_export.model.datapoint_collection import DatapointCollection
from napytau.util.model.value_error_pair import ValueErrorPair


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self) -> None:
        """
        Constructor for the GUIApp, initializes the GUI.
        This is the logical entry point into the GUI.
        """
        super().__init__()

        # Datapoints
        self.datapoints: DatapointCollection = DatapointCollection([])
        self.datapoints_for_fitting: DatapointCollection = DatapointCollection([])
        self.datapoints_for_calculation: DatapointCollection = DatapointCollection([])

        # values
        self.tau = tk.IntVar()
        self.tau.set(2)

        # configure window
        self.title("NaPyTau")
        width = 1366
        height = 768
        self.geometry(f"{width}x{height}")

        """
        Configure grid. Current Layout:
        Three rows, two columns with
        - Graph from row 0 to 1, column 0
        - Checkbox panel in row 0, column 1
        - Control panel from row 1 to 2, column 1
        - Logger in row 2, column 0
        """
        # Row ratio: 3/8, 3/8, 1/4
        total_height = 8  # 3+3+2 = 8 parts
        self.grid_rowconfigure(0, weight=3, minsize=3 * height // total_height)
        # Reduce graph height by 30 to asure all components and their
        # separators are inside the window.
        self.grid_rowconfigure(1, weight=3, minsize=3 * height // total_height - 30)
        self.grid_rowconfigure(2, weight=2, minsize=2 * height // total_height)

        # column ratio: 2/3, 1/3
        total_width = 3  # 2+1 = 3 parts
        # Reduce graph width by 30 to asure all components and their
        # separators are inside the window.
        self.grid_columnconfigure(0, weight=2, minsize=2 * width // total_width - 30)
        self.grid_columnconfigure(1, weight=1, minsize=1 * width // total_width)

        # Define menu bar callback functions
        menu_bar_callbacks = {
            "open_file": self.open_file,
            "save_file": self.save_file,
            "read_setup": self.read_setup,
            "quit": self.quit,
            "change_appearance_mode": self.change_appearance_mode,
            "select_number_of_polynomials": self.select_number_of_polynomials,
            "select_polynomial_mode": self.select_polynomial_mode,
            "select_alpha_calc_mode": self.select_alpha_calc_mode,
        }

        # Initialize the menu bar
        self.menu_bar = MenuBar(self, menu_bar_callbacks)

        # Initialize the checkbox panel
        self.checkbox_panel = CheckboxPanel(self)

        # Update data checkboxes with some data to create them.
        # TODO: Remove dummy points later on.
        self.update_data_checkboxes(
            [
                create_dummy_datapoint(
                    ValueErrorPair(1.0, 0.3), ValueErrorPair(5.0, 1.0)
                ),
                create_dummy_datapoint(
                    ValueErrorPair(2.0, 0.3), ValueErrorPair(1.0, 2.0)
                ),
                create_dummy_datapoint(
                    ValueErrorPair(3.0, 0.3), ValueErrorPair(3.0, 3.0)
                ),
                create_dummy_datapoint(
                    ValueErrorPair(4.0, 0.3), ValueErrorPair(9.0, 4.0)
                ),
                create_dummy_datapoint(
                    ValueErrorPair(5.0, 0.3), ValueErrorPair(7.0, 5.0)
                ),
                create_dummy_datapoint(
                    ValueErrorPair(6.0, 0.3), ValueErrorPair(2.0, 6.0)
                ),
                create_dummy_datapoint(
                    ValueErrorPair(7.0, 0.3), ValueErrorPair(1.0, 7.0)
                ),
                create_dummy_datapoint(
                    ValueErrorPair(8.0, 0.3), ValueErrorPair(10.0, 8.0)
                ),
                create_dummy_datapoint(
                    ValueErrorPair(9.0, 0.3), ValueErrorPair(5.0, 9.0)
                ),
                create_dummy_datapoint(
                    ValueErrorPair(10.0, 0.3), ValueErrorPair(4.0, 10.0)
                ),
            ]
        )

        # Initialize the graph
        self.graph: Graph = Graph(self)

        self.toolbar: Toolbar = Toolbar(self, self.graph.canvas)

        # Initialize the control panel
        self.control_panel = ControlPanel(self)

        # Initialize the logger
        self.logger = Logger(self)

    def open_file(self) -> None:
        """
        Opens the file explorer and lets the user choose a file to open.
        """
        file_path = filedialog.askopenfilename(
            title="Choose file",
            filetypes=[
                ("ALl files", "*.*"),
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
            ],
        )

        if file_path:
            self.logger.log_message(f"chosen file: {file_path}", LogMessageType.INFO)

    def save_file(self) -> None:
        """
        Saves the file.
        """
        self.logger.log_message("Saved file", LogMessageType.SUCCESS)

    def read_setup(self) -> None:
        """
        Reads the setup.
        """
        self.logger.log_message("read setup not implemented yet.", LogMessageType.INFO)

    def quit(self) -> None:
        """
        Quits the program.
        """
        self.destroy()

    def change_appearance_mode(self) -> None:
        """
        Changes the appearance mode to the variable appearance_mode.
        """
        customtkinter.set_appearance_mode(self.menu_bar.appearance_mode.get())
        self.logger.switch_logger_appearance(self.menu_bar.appearance_mode.get())

        self.graph.update_plot()

    def select_number_of_polynomials(self) -> None:
        """
        Selects the number of polynomials to use.
        """
        self.logger.log_message(
            "selected number of polynomials: "
            + self.menu_bar.number_of_polynomials.get()
            + " but not implemented yet!",
            LogMessageType.INFO,
        )

    def select_polynomial_mode(self) -> None:
        """
        Selects the polynomial mode.
        """
        self.logger.log_message(
            "Polynomials set to "
            + self.menu_bar.polynomial_mode.get()
            + " but not implemented yet!",
            LogMessageType.ERROR,
        )

    def select_alpha_calc_mode(self) -> None:
        """
        Selects the alpha calculation mode.
        """
        self.logger.log_message(
            "Alpha calculation set to "
            + self.menu_bar.alpha_calc_mode.get()
            + " but not implemented yet!",
            LogMessageType.ERROR,
        )

    def update_data_checkboxes(self, new_datapoints: List[Datapoint]) -> None:
        """
        Updates the datapoint for the gui and updates both columns of the
        data checkboxes.
        Call this method if there are new datapoints.
        :param new_datapoints: The new list of datapoints.
        """
        self.datapoints = DatapointCollection(new_datapoints)

        for point in new_datapoints:
            self.datapoints_for_fitting.add_datapoint(point)
            self.datapoints_for_calculation.add_datapoint(point)

        self.checkbox_panel.update_data_checkboxes_fitting()
        self.checkbox_panel.update_data_checkboxes_calculation()


"""
Function for testing purposes only!
"""


def create_dummy_datapoint(
    distance: ValueErrorPair, shifted_intensity: ValueErrorPair
) -> Datapoint:
    datapoint = Datapoint(distance)
    datapoint.shifted_intensity = shifted_intensity
    datapoint.unshifted_intensity = ValueErrorPair(0.0, 0.0)
    return datapoint


def init(cli_arguments: CLIArguments) -> None:
    app = App()
    app.mainloop()
