import tkinter as tk
from tkinter import Menu
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.


class MenuBar:
    def __init__(self, parent: "App", callbacks: dict) -> None:
        """
        Initializes the menu bar and its items.
        :param parent: Parent widget to host the checkbox panel.
        :param callbacks: The dictionary of callback functions for the menu bar.
        """
        self.parent = parent
        self.callbacks = callbacks

        # Create menu bar
        self.menubar = Menu(parent)
        parent.config(menu=self.menubar)

        # Initialize menus
        self._init_file_menu()
        self._init_view_menu()
        self._init_poly_menu()
        self._init_alpha_calc_menu()

    def _init_file_menu(self) -> None:
        """
        Create the File menu.
        """
        file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Open", command=self.callbacks["open_file"])
        file_menu.add_command(label="Save", command=self.callbacks["save_file"])
        file_menu.add_command(label="Read Setup", command=self.callbacks["read_setup"])
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.callbacks["quit"])

    def _init_view_menu(self) -> None:
        """
        Create the View menu.
        """
        view_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=view_menu)

        self.appearance_mode = tk.StringVar(value="system")  # Default: system
        view_menu.add_radiobutton(
            label="Light mode",
            variable=self.appearance_mode,
            value="light",
            command=self.callbacks["change_appearance_mode"],
        )
        view_menu.add_radiobutton(
            label="Dark mode",
            variable=self.appearance_mode,
            value="dark",
            command=self.callbacks["change_appearance_mode"],
        )
        view_menu.add_radiobutton(
            label="System",
            variable=self.appearance_mode,
            value="system",
            command=self.callbacks["change_appearance_mode"],
        )

    def _init_poly_menu(self) -> None:
        """
        Create the Polynomials menu.
        """
        poly_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Polynomials", menu=poly_menu)

        number_of_polys_menu = Menu(poly_menu, tearoff=0)
        poly_menu.add_cascade(label="Number of Polynomials", menu=number_of_polys_menu)

        self.number_of_polynomials = tk.StringVar(value="3")  # Default: 3 Polynomials
        for i in range(1, 11):
            number_of_polys_menu.add_radiobutton(
                label=str(i),
                variable=self.number_of_polynomials,
                value=str(i),
                command=self.callbacks["select_number_of_polynomials"],
            )
        poly_menu.add_separator()

        self.polynomial_mode = tk.StringVar(value="Exponential")  # Default: Exponential
        poly_menu.add_radiobutton(
            label="Equidistant",
            variable=self.polynomial_mode,
            value="Equidistant",
            command=self.callbacks["select_polynomial_mode"],
        )
        poly_menu.add_radiobutton(
            label="Exponential",
            variable=self.polynomial_mode,
            value="Exponential",
            command=self.callbacks["select_polynomial_mode"],
        )

    def _init_alpha_calc_menu(self) -> None:
        """
        Create the Alpha Calculation menu.
        """
        alpha_calc_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Alpha calculation", menu=alpha_calc_menu)

        self.alpha_calc_mode = tk.StringVar(value="sum ratio")
        alpha_calc_menu.add_radiobutton(
            label="Sum Ratio",
            variable=self.alpha_calc_mode,
            value="sum ratio",
            command=self.callbacks["select_alpha_calc_mode"],
        )
        alpha_calc_menu.add_radiobutton(
            label="Weighted Mean",
            variable=self.alpha_calc_mode,
            value="weighted mean",
            command=self.callbacks["select_alpha_calc_mode"],
        )
