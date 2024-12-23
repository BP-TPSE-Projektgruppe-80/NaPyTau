from typing import List, Tuple

import tkinter as tk
from tkinter import filedialog

import customtkinter

from napytau.cli.cli_arguments import CLIArguments

from napytau.gui.components.checkbox_panel import CheckboxPanel
from napytau.gui.components.control_panel import ControlPanel
from napytau.gui.components.graph import Graph
from napytau.gui.components.logger import Logger
from napytau.gui.components.menu_bar import MenuBar
from napytau.gui.model.checkbox_datapoint import CheckboxDataPoint
from napytau.import_export.model.datapoint import Datapoint
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
        self.datapoints: List[Datapoint] = []
        self.datapoints_for_fitting: List[CheckboxDataPoint] = []
        self.datapoints_for_calculation: List[CheckboxDataPoint] = []

        # values
        self.tau = tk.IntVar()
        self.tau.set(2)

        # configure window
        self.title("NaPyTau")
        self.geometry("1366x768")

        """
        Configure grid. Current Layout:
        Three rows, two columns with
        - Graph from row 0 to 1, column 0
        - Checkboxes in row 0, column 1
        - Control area in row 1, column 1
        - Information area in row 2, column 0 to 1
        """
        self.grid_rowconfigure((0, 2), weight=1)  # Three rows
        self.grid_columnconfigure((0, 1), weight=1)  # Two columns

        # Weights are adjusted
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=1)

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

                create_dummy_datapoint(ValueErrorPair(1.0, 0.3),
                                       ValueErrorPair(5.0, 1.0)),
                create_dummy_datapoint(ValueErrorPair(2.0, 0.3),
                                       ValueErrorPair(1.0, 2.0)),
                create_dummy_datapoint(ValueErrorPair(3.0, 0.3),
                                       ValueErrorPair(3.0, 3.0)),
                create_dummy_datapoint(ValueErrorPair(4.0, 0.3),
                                       ValueErrorPair(9.0, 4.0)),
                create_dummy_datapoint(ValueErrorPair(5.0, 0.3),
                                       ValueErrorPair(7.0, 5.0)),
                create_dummy_datapoint(ValueErrorPair(6.0, 0.3),
                                       ValueErrorPair(2.0, 6.0)),
                create_dummy_datapoint(ValueErrorPair(7.0, 0.3),
                                       ValueErrorPair(1.0, 7.0)),
                create_dummy_datapoint(ValueErrorPair(8.0, 0.3),
                                       ValueErrorPair(10.0, 8.0)),
                create_dummy_datapoint(ValueErrorPair(9.0, 0.3),
                                       ValueErrorPair(5.0, 9.0)),
                create_dummy_datapoint(ValueErrorPair(10.0, 0.3),
                                       ValueErrorPair(4.0, 10.0)),


            ]
        )

        # Initialize the graph
        self.graph = Graph(self)

        # Initialize the control panel
        self.control_panel = ControlPanel(self)

        # Initialize the logger
        self.logger = Logger(self)

    def open_file(self) -> None:
        """
        Opens the file explorer and lets the user choose a file to open.
        """
        print("open_file")
        file_path = filedialog.askopenfilename(
            title="Choose file",
            filetypes=[
                ("ALl files", "*.*"),
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
            ],
        )

        if file_path:
            print(f"chosen file: {file_path}")

    def save_file(self) -> None:
        """
        Saves the file.
        """
        print("save_file")

    def read_setup(self) -> None:
        """
        Reads the setup.
        """
        print("read_setup")

    def quit(self) -> None:
        """
        Quits the program.
        """
        print("quit")
        self.destroy()

    def change_appearance_mode(self) -> None:
        """
        Changes the appearance mode to the variable appearance_mode.
        """
        customtkinter.set_appearance_mode(self.menu_bar.appearance_mode.get())

        self.graph.update_plot()

    def select_number_of_polynomials(self) -> None:
        """
        Selects the number of polynomials to use.
        """
        print(
            "selected number of polynomials: "
            + self.menu_bar.number_of_polynomials.get()
        )

    def select_polynomial_mode(self) -> None:
        """
        Selects the polynomial mode.
        """
        print("select polynomial mode " + self.menu_bar.polynomial_mode.get())

    def select_alpha_calc_mode(self) -> None:
        """
        Selects the alpha calculation mode.
        """
        print("select alpha calc mode " + self.menu_bar.alpha_calc_mode.get())

    def update_data_checkboxes(self, new_datapoints: List[Datapoint]) -> None:
        """
        Updates the datapoint for the gui and updates both columns of the
        data checkboxes.
        Call this method if there are new datapoints.
        :param new_datapoints: The new list of datapoints.
        """
        self.datapoints = new_datapoints.copy()

        for point in new_datapoints:
            self.datapoints_for_fitting.append(CheckboxDataPoint(point, True))
            self.datapoints_for_calculation.append(CheckboxDataPoint(point, True))

        self.checkbox_panel.update_data_checkboxes_fitting()
        self.checkbox_panel.update_data_checkboxes_calculation()

"""
Function for testing purposes only!
"""

def create_dummy_datapoint(distance: ValueErrorPair,
                           shifted_intensity: ValueErrorPair
                           ) -> Datapoint:

    datapoint = Datapoint(distance)
    datapoint.shifted_intensity = shifted_intensity
    datapoint.unshifted_intensity = ValueErrorPair(0.0,0.0)
    return datapoint


def init(cli_arguments: CLIArguments) -> None:
    app = App()
    app.mainloop()

