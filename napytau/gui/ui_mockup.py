from typing import List, Tuple

import tkinter as tk
from tkinter import Canvas

import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from napytau.cli.cli_arguments import CLIArguments
from napytau.core.logic_mockup import logic
from tkinter import Menu

from napytau.gui.checkbox_datapoint import CheckboxDataPoint

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


def plot(value, window) -> Canvas:
    # the figure that will contain the plot
    fig = Figure(figsize=(3, 2), dpi=100, facecolor="white", edgecolor="black")

    # list of squares
    y = [(i - 50) ** value for i in range(101)]

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(y)

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    return canvas.get_tk_widget()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Datapoints
        self.datapoints: List[Tuple[float, float]]=[]
        self.datapoints_for_fitting: List[CheckboxDataPoint]=[]
        self.datapoints_for_calculation: List[CheckboxDataPoint]=[]

        # values

        self.tau = tk.IntVar()
        self.tau.set(2)

        # configure window
        self.title("NaPyTau")
        #self.geometry(f"{1100}x{580}")
        self.geometry("1366x768")

        self.grid_columnconfigure((0, 1), weight=1)  # Two columns
        self.grid_rowconfigure((0, 2), weight=1)  # Three rows

        # Weights are adjusted
        self.grid_columnconfigure(0, weight=8)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)


        # Create menu bar
        menubar = Menu(self)
        self.config(menu=menubar)

        # =======================================
        #  Create Button "File" in menu bar
        # =======================================
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Read Setup", command=self.read_setup)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # =======================================
        #  Create button "View" in menu bar
        # =======================================
        view_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)

        self.appearance_mode = tk.StringVar(value="system")  # Default: system
        view_menu.add_radiobutton(
            label="Light mode",
            variable=self.appearance_mode,
            value="light",
            command=self.change_appearance_mode)
        view_menu.add_radiobutton(
            label="Dark mode",
            variable=self.appearance_mode,
            value="dark",
            command=self.change_appearance_mode)
        view_menu.add_radiobutton(
            label="System",
            variable=self.appearance_mode,
            value="system",
            command=self.change_appearance_mode)

        # =======================================
        #  Create button "Polynomials" in menu bar
        # =======================================
        poly_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Polynomials", menu=poly_menu)
        number_of_polys_menu = Menu(poly_menu, tearoff=0)
        poly_menu.add_cascade(label="Number of Polynomials", menu=number_of_polys_menu)

        self.number_of_polynomials = tk.StringVar(value="3")  # Default: 3 Polynomials
        for i in range(1, 11):
            number_of_polys_menu.add_radiobutton(
                label=str(i),
                variable=self.number_of_polynomials,
                value=str(i),
                command=self.select_number_of_polynomials)
        poly_menu.add_separator()
        self.polynomial_mode = tk.StringVar(value="Exponential")  # Default: Exponential
        poly_menu.add_radiobutton(
            label="Equidistant",
            variable=self.polynomial_mode,
            value="Equidistant",
            command=self.select_polynomial_mode)
        poly_menu.add_radiobutton(
            label="Exponential",
            variable=self.polynomial_mode,
            value="Exponential",
            command=self.select_polynomial_mode)

        # =======================================
        #  Create button "Alpha calculation" in menu bar
        # =======================================
        alpha_calc_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Alpha calculation", menu=alpha_calc_menu)

        self.alpha_calc_mode = tk.StringVar(value="sum ratio")
        alpha_calc_menu.add_radiobutton(
            label="Sum Ratio",
            variable=self.alpha_calc_mode,
            value="sum ratio",
            command=self.select_alpha_calc_mode)
        alpha_calc_menu.add_radiobutton(
            label="Weighted Mean",
            variable=self.alpha_calc_mode,
            value="weighted mean",
            command=self.select_alpha_calc_mode)

        # Left upper corner: Graph
        self.graph_frame = plot(self.tau.get(), self)
        self.graph_frame.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=10,
            pady=10,
            sticky="nsew")
        self.graph_frame.grid_propagate(False)
        graph_label = customtkinter.CTkLabel(
            self.graph_frame,
            text="Graph-Area",
            anchor="center")
        graph_label.pack(expand=True)

        # Right upper corner: Checkboxes with datapoints
        self.frame_datapoint_checkboxes = customtkinter.CTkFrame(
            self,
            width=300,
            height=200,
            corner_radius=10)
        self.frame_datapoint_checkboxes.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew")
        self.frame_datapoint_checkboxes.grid_propagate(False)

        # TODO: Remove dummy points later on.
        self.update_data_checkboxes([
            (1.0, 5.23),
            (2.0, 7.1),
            (3.0, 0.44),
            (4.0, 12.76),
            (5.0, 5.0),
            (6.0, 4.93),
            (7.0, 2.7),
            (8.0, 7.1),
            (9.0, 9.52),
            (10.0, 1.85)])

        # Below checkboxes: Buttons for calculation
        self.button_area = customtkinter.CTkFrame(self, corner_radius=10)
        self.button_area.grid(
            row=1,
            column=1,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew")
        self.button_area.grid_rowconfigure((0, 1), weight=1)
        self.button_area.grid_propagate(True)

        # Scaling menu
        self.scaling_label = customtkinter.CTkLabel(
            self.button_area, text="UI Scaling:", anchor="nw"
        )
        self.scaling_label.grid(row=0, column=0, padx=10, pady=10)
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.button_area,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=0, column=1, padx=20, pady=(10, 20))
        self.scaling_optionemenu.set("100%")

        # Calculation
        self.entry = customtkinter.CTkEntry(self.button_area, textvariable=self.tau)
        self.entry.grid(
            row=1, column=0, padx=10, pady=10#, sticky="nsew"
        )

        self.main_button_1 = customtkinter.CTkButton(
            self.button_area,
            fg_color="transparent",
            border_width=1,
            text="calc",
            text_color=("gray10", "#DCE4EE"),
            command=self.calc,
        )
        self.main_button_1.grid(
            row=1, column=1, padx=10, pady=10, sticky="nsew"
        )
        self.label = customtkinter.CTkLabel(self.button_area, width=200)
        self.label.grid(
            row=2, column=0, columnspan=1, padx=10, pady=10, sticky="nsew"
        )
        self.label.configure(text="Result: ")


        # Bottom: Output field for errors or information of tau and delta-tau
        self.output_frame = customtkinter.CTkFrame(self, height=100, corner_radius=10)
        self.output_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew")
        self.output_frame.grid_propagate(False)

        self.output_label = customtkinter.CTkLabel(
            self.output_frame, text="Error messages etc. will be shown here", anchor="w"
        )
        self.output_label.pack(fill="both", padx=10, pady=10)


    def open_file(self):
        """
        Opens the file explorer.
        """
        print("open_file")

    def save_file(self):
        """
        Saves the file.
        """
        print("save_file")

    def read_setup(self):
        """
        Reads the setup.
        """
        print("read_setup")

    def quit(self):
        """
        Quits the program.
        """
        print("quit")
        self.destroy()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_appearance_mode(self):
        """
        Changes the appearance mode to the variable appearance_mode.
        """
        customtkinter.set_appearance_mode(self.appearance_mode.get())
        print("change appearance mode to " + self.appearance_mode.get())

    def select_number_of_polynomials(self):
        """
        Selects the number of polynomials to use.
        """
        print("selected number of polynomials: " + self.number_of_polynomials.get())

    def select_polynomial_mode(self):
        """
        Selects the polynomial mode.
        """
        print("select polynomial mode " + self.polynomial_mode.get())

    def select_alpha_calc_mode(self):
        """
        Selects the alpha calculation mode.
        """
        print("select alpha calc mode " + self.alpha_calc_mode.get())

    def _update_data_checkboxes_fitting(self):
        """
        Do not call from outside. Updates the checkboxes with data points
        for the fitting.
        """
        # Clear all checkboxes for the fitting
        for widget in self.frame_datapoint_checkboxes.winfo_children():
            if widget.grid_info().get("column") == 0: # Column 0 for fitting
                widget.grid_forget()

        header_label = customtkinter.CTkLabel(
            self.frame_datapoint_checkboxes,
            text="Datapoints for fitting",
            font=("Arial", 16))
        header_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Update all checkboxes for the fitting
        for i in range(len(self.datapoints)):
            x, y = self.datapoints[i]

            checkbox = customtkinter.CTkCheckBox(
                self.frame_datapoint_checkboxes,
                text=f"({x} | {y})",
                variable=customtkinter.IntVar(value=1),
                command=lambda index=i: self._data_checkbox_fitting_event(index))
            checkbox.grid(row=i+1, column=0, padx=10, pady=2, sticky="nsew")

    def _data_checkbox_fitting_event(self, index):
        """
        Do not call from outside. Is called if a data checkbox
        for the fitting is called.
        Toggles the intern boolean value of the datapoint.
        :param index: Index of the pressed data checkbox.
        """
        self.datapoints_for_fitting[index].is_checked =\
            not self.datapoints_for_fitting[index].is_checked
        if self.datapoints_for_fitting[index].is_checked:
            print("[fitting] checkbox with index " + str(index) + " activated.")
        else:
            print("[fitting] checkbox with index " + str(index) + " deactivated.")

    def _update_data_checkboxes_calculation(self):
        """
        Do not call from outside. Updates the checkboxes with data points for
        the calculation of tau and delta-tau.
        """
        # Clear all checkboxes for the calculation
        for widget in self.frame_datapoint_checkboxes.winfo_children():
            if widget.grid_info().get("column") == 1:
                widget.grid_forget()

        header_label = customtkinter.CTkLabel(
            self.frame_datapoint_checkboxes,
            text="Datapoints for tau calculation",
            font=("Arial", 16))
        header_label.grid(row=0, column=1, padx=30, pady=5, sticky="nsew")

        # Update all checkboxes for the calculation
        for i in range(len(self.datapoints)):
            x, y = self.datapoints[i]

            checkbox = customtkinter.CTkCheckBox(
                self.frame_datapoint_checkboxes,
                text=f"({x} | {y})",
                variable=customtkinter.IntVar(value=1),
                command=lambda index=i: self._data_checkbox_calculation_event(index))
            checkbox.grid(row=i + 1, column=1, padx=35, pady=2, sticky="nsew")

    def _data_checkbox_calculation_event(self, index):
        """
        Do not call from outside. Is called if a data checkbox for the calculation
        of tau and delta-tau is called.
        Toggles the intern boolean value of the datapoint.
        :param index: Index of the pressed data checkbox.
        """
        self.datapoints_for_calculation[index].is_checked = \
            not self.datapoints_for_calculation[index].is_checked
        if self.datapoints_for_calculation[index].is_checked:
            print("[calculation] checkbox with index " + str(index) + " activated.")
        else:
            print("[calculation] checkbox with index " + str(index) + " deactivated.")

    def update_data_checkboxes(self, new_datapoints: List[Tuple[float, float]]):
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

        self._update_data_checkboxes_fitting()
        self._update_data_checkboxes_calculation()

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def use_slider_value(self, _value):
        self.calc()

    def calc(self):
        entry_value = self.tau.get()

        self.label.configure(text=f"Result: {logic(entry_value)}")


def init(cli_arguments: CLIArguments):
    app = App()
    app.mainloop()
