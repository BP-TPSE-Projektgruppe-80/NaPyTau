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
        self.datapoints: List[Tuple[float, float]] = []
        self.datapoints_for_fitting: List[CheckboxDataPoint] = []
        self.datapoints_for_calculation: List[CheckboxDataPoint] = []

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
        self.grid_rowconfigure(1, weight=3, minsize=3 * height // total_height -30)
        self.grid_rowconfigure(2, weight=2, minsize=2 * height // total_height)

        # column ratio: 2/3, 1/3
        total_width = 3  # 2+1 = 3 parts
        # Reduce graph width by 30 to asure all components and their
        # separators are inside the window.
        self.grid_columnconfigure(0, weight=2, minsize=2 * width // total_width -30)
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

        # Initialize the graph
        self.graph = Graph(self)

        # Initialize the checkbox panel
        self.checkbox_panel = CheckboxPanel(self)

        # Update data checkboxes with some data to create them.
        # TODO: Remove dummy points later on.
        self.update_data_checkboxes(
            [
                (1.0, 5.23),
                (2.0, 7.1),
                (3.0, 0.44),
                (4.0, 12.76),
                (5.0, 5.0),
                (6.0, 4.93),
                (7.0, 2.7),
                (8.0, 7.1),
                (9.0, 9.52),
                (10.0, 1.85),
            ]
        )

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
        self.logger.change_logger_appearance(self.menu_bar.appearance_mode.get())

        self.graph.update_plot()

    def select_number_of_polynomials(self) -> None:
        """
        Selects the number of polynomials to use.
        """
        print("selected number of polynomials: "
              + self.menu_bar.number_of_polynomials.get())
        self.logger.log_info("selected number of polynomials: "
              + self.menu_bar.number_of_polynomials.get()
              + " but not implemented yet!")

    def select_polynomial_mode(self) -> None:
        """
        Selects the polynomial mode.
        """
        print("select polynomial mode " + self.menu_bar.polynomial_mode.get())
        self.logger.log_error("Polynomials set to "
                              + self.menu_bar.polynomial_mode.get()
                              + " but not implemented yet!")

    def select_alpha_calc_mode(self) -> None:
        """
        Selects the alpha calculation mode.
        """
        print("select alpha calc mode " + self.menu_bar.alpha_calc_mode.get())
        self.logger.log_error("Alpha calculation set to "
                              + self.menu_bar.alpha_calc_mode.get()
                              + " but not implemented yet!")

    def update_data_checkboxes(self, new_datapoints: List[Tuple[float, float]]) -> None:
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


def init(cli_arguments: CLIArguments) -> None:
    app = App()
    app.mainloop()
