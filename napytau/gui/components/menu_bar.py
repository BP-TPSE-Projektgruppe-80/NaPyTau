import tkinter as tk
import customtkinter
from tkinter import Menu
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.

class MenuBar(customtkinter.CTkFrame):
    def __init__(self, parent: "App", callbacks: dict) -> None:
        """
        Initializes the menu bar and its items.
        :param parent: Parent widget to host the menubar.
        :param callbacks: The dictionary of callback functions for the menu bar.
        """
        super().__init__(parent)
        self.callbacks = callbacks

        # Setting up default values
        self.appearance_mode = tk.StringVar(value="system")
        self.number_of_polynomials = tk.StringVar(value="3")
        self.alpha_calc_mode = tk.StringVar(value="sum ratio")
        self.polynomial_mode = tk.StringVar(value="Exponential")

        self.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.pack_propagate(False)

        self._create_file_button()
        self._create_view_button()
        self._create_polynomial_button()
        self._create_alpha_calc_button()

    def _create_file_button(self) -> None:
        self.file_button = customtkinter.CTkButton(self, text="File", command=self.open_file_menu)
        self.file_button.grid(row=0, column=0, padx=5, pady=5)

        self.file_menu = tk.Menu(self, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.callbacks["open_file"])
        self.file_menu.add_command(label="Save", command=self.callbacks["save_file"])
        self.file_menu.add_command(label="Read Setup", command=self.callbacks["read_setup"])
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.callbacks["quit"])

    def _create_view_button(self) -> None:
        self.view_button = customtkinter.CTkButton(self, text="View", command=self.open_view_menu)
        self.view_button.grid(row=0, column=1, padx=5, pady=5)

        self.view_menu = tk.Menu(self, tearoff=0)
        self.view_menu.add_radiobutton(label="Light Mode", variable=self.appearance_mode, value="light",
                                  command=self.callbacks["change_appearance_mode"])
        self.view_menu.add_radiobutton(label="Dark Mode", variable=self.appearance_mode, value="dark",
                                  command=self.callbacks["change_appearance_mode"])
        self.view_menu.add_radiobutton(label="System Mode", variable=self.appearance_mode, value="system",
                                  command=self.callbacks["change_appearance_mode"])

    def _create_polynomial_button(self) -> None:
        self.polynomial_button = customtkinter.CTkButton(self, text="Polynomials", command=self.open_polynomial_menu)
        self.polynomial_button.grid(row=0, column=2, padx=5, pady=5)

        self.polynomial_menu = tk.Menu(self, tearoff=0)
        number_of_polys_menu = Menu(self.polynomial_menu, tearoff=0)
        self.polynomial_menu.add_cascade(label="Number of Polynomials", menu=number_of_polys_menu)

        for i in range(1, 11):
            number_of_polys_menu.add_radiobutton(
                label=str(i),
                variable=self.number_of_polynomials,
                value=str(i),
                command=self.callbacks["select_number_of_polynomials"],
            )
        self.polynomial_menu.add_separator()

        self.polynomial_menu.add_radiobutton(
            label="Equidistant",
            variable=self.polynomial_mode,
            value="Equidistant",
            command=self.callbacks["select_polynomial_mode"],
        )
        self.polynomial_menu.add_radiobutton(
            label="Exponential",
            variable=self.polynomial_mode,
            value="Exponential",
            command=self.callbacks["select_polynomial_mode"],
        )

    def _create_alpha_calc_button(self):
        self.alpha_calc_button = customtkinter.CTkButton(self, text="Alpha calculation", command=self.open_alpha_calc_menu)
        self.alpha_calc_button.grid(row=0, column=3, padx=5, pady=5)

        self.alpha_calc_menu = tk.Menu(self, tearoff=0)
        self.alpha_calc_menu.add_radiobutton(
            label="Sum Ratio",
            variable=self.alpha_calc_mode,
            value="sum ratio",
            command=self.callbacks["select_alpha_calc_mode"],
        )
        self.alpha_calc_menu.add_radiobutton(
            label="Weighted Mean",
            variable=self.alpha_calc_mode,
            value="weighted mean",
            command=self.callbacks["select_alpha_calc_mode"],
        )

    def open_file_menu(self):
        self.file_menu.post(self.file_button.winfo_rootx(),
                            self.file_button.winfo_rooty() + self.file_button.winfo_height())

    def open_view_menu(self):
        self.view_menu.post(self.view_button.winfo_rootx(),
                            self.view_button.winfo_rooty() + self.view_button.winfo_height())

    def open_polynomial_menu(self):
        self.polynomial_menu.post(self.polynomial_button.winfo_rootx(),
                            self.polynomial_button.winfo_rooty() + self.polynomial_button.winfo_height())

    def open_alpha_calc_menu(self):
        self.alpha_calc_menu.post(self.alpha_calc_button.winfo_rootx(),
                            self.alpha_calc_button.winfo_rooty() + self.alpha_calc_button.winfo_height())
