import tkinter as tk
import customtkinter
from tkinter import Menu
from typing import TYPE_CHECKING

from napytau.import_export.import_export import (
    IMPORT_FORMAT_NAPYTAU,
    IMPORT_FORMAT_LEGACY,
)

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.


def open_dropdown_menu(dropdown_menu: tk.Menu, button: customtkinter.CTkButton) -> None:
    """
    On the given dropdown menu on the position of the given button.
    :param dropdown_menu: The dropdown menu to open.
    :param button: The button on which position the menu will be opened.
    """
    dropdown_menu.post(
        button.winfo_rootx(), button.winfo_rooty() + button.winfo_height()
    )


class MenuBar(customtkinter.CTkFrame):
    def __init__(self, parent: "App", callbacks: dict) -> None:
        """
        Initializes the menu bar and its items.
        :param parent: Parent widget to host the menubar.
        :param callbacks: The dictionary of callback functions for the menu bar.
        """
        super().__init__(parent)
        self.callbacks = callbacks

        self.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.pack_propagate(False)

        # Initialize menus
        self._init_file_menu()
        self._init_view_menu()
        self._init_poly_menu()
        self._init_alpha_calc_menu()
        self._init_mode_menu()

        self._create_file_button()
        self._create_view_button()
        self._create_polynomial_button()
        self._create_alpha_calc_button()

    def _create_file_button(self) -> None:
        """
        Creates the button in the menubar for all file operations.
        """
        self.file_menu = tk.Menu(self, tearoff=0)

        # Declare file_button in advance for type checking
        self.file_button: customtkinter.CTkButton | None = None

        file_menu.add_command(
            label="Open",
            command=lambda: self.callbacks["open_directory"](self.mode.get()),
        )
        # TODO: Connect after export is implemented
        file_menu.add_command(
            label="Save", command=lambda: self.callbacks["save_file"](self.mode.get())
        )
        file_menu.add_command(
            label="Read Setup",
            command=lambda: self.callbacks["read_setup"](self.mode.get()),
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.callbacks["quit"])

    def _create_view_button(self) -> None:
        """
        Creates the view button in the menubar.
        """
        self.view_menu = tk.Menu(self, tearoff=0)

        # Declare view_button in advance for type checking
        self.view_button: customtkinter.CTkButton | None = None

        self.view_button = customtkinter.CTkButton(
            self,
            text="View",
            command=lambda: open_dropdown_menu(self.view_menu, self.view_button),
        )
        self.view_button.grid(row=0, column=1, padx=5, pady=5)

        self.view_menu.add_radiobutton(
            label="Light Mode",
            variable=self.appearance_mode,
            value="light",
            command=self.callbacks["change_appearance_mode"],
        )
        self.view_menu.add_radiobutton(
            label="Dark Mode",
            variable=self.appearance_mode,
            value="dark",
            command=self.callbacks["change_appearance_mode"],
        )
        self.view_menu.add_radiobutton(
            label="System Mode",
            variable=self.appearance_mode,
            value="system",
            command=self.callbacks["change_appearance_mode"],
        )

    def _create_polynomial_button(self) -> None:
        """
        Creates the button for the polynomial settings in the menubar.
        """
        self.polynomial_menu = tk.Menu(self, tearoff=0)

        # Declare polynomial_button in advance for type checking
        self.polynomial_button: customtkinter.CTkButton | None = None

        self.polynomial_button = customtkinter.CTkButton(
            self,
            text="Polynomials",
            command=lambda: open_dropdown_menu(
                self.polynomial_menu, self.polynomial_button
            ),
        )
        self.polynomial_button.grid(row=0, column=2, padx=5, pady=5)

        number_of_polys_menu = Menu(self.polynomial_menu, tearoff=0)
        self.polynomial_menu.add_cascade(
            label="Number of Polynomials", menu=number_of_polys_menu
        )

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

    def _create_alpha_calc_button(self) -> None:
        """
        Creates the button for the alpha calculation settings in the menubar.
        """
        self.alpha_calc_menu = tk.Menu(self, tearoff=0)

        # Declare alpha_calc_button in advance for type checking
        self.alpha_calc_button: customtkinter.CTkButton | None = None

        self.alpha_calc_button = customtkinter.CTkButton(
            self,
            text="Alpha calculation",
            command=lambda: open_dropdown_menu(
                self.alpha_calc_menu, self.alpha_calc_button
            ),
        )
        self.alpha_calc_button.grid(row=0, column=3, padx=5, pady=5)

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

    def _init_mode_menu(self) -> None:
        """
        Create the Mode menu. Allowing the user to switch the import/export mode
        between `legacy` and `napytau`.
        """

        mode_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Mode", menu=mode_menu)

        self.mode = tk.StringVar(value=IMPORT_FORMAT_NAPYTAU)
        mode_menu.add_radiobutton(
            label="Legacy",
            variable=self.mode,
            value=IMPORT_FORMAT_LEGACY,
        )
        mode_menu.add_radiobutton(
            label="Napytau",
            variable=self.mode,
            value=IMPORT_FORMAT_NAPYTAU,
        )
