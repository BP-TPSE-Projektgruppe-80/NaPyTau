import tkinter as tk
import customtkinter
from napytau.core.logic_mockup import logic
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.


class ControlPanel(customtkinter.CTkFrame):
    def __init__(self, parent: "App"):
        """
        Initializes the control panel .
        :param parent: Parent widget to host the control panel.
        """
        super().__init__(parent, corner_radius=10)
        self.parent = parent

        # Main area for buttons and controls
        self.grid(row=1, column=1, rowspan=2, padx=(0, 10), pady=(10, 10),
                  sticky="nsew")
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_propagate(True)

        # Scaling menu
        self.scaling_label = customtkinter.CTkLabel(
            self, text="UI Scaling:", anchor="nw"
        )
        self.scaling_label.grid(row=0, column=0, padx=10, pady=10)

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=0, column=1, padx=20, pady=(10, 20))
        self.scaling_optionemenu.set("100%")

        # Calculation Entry and Button
        self.tau = tk.StringVar()  # Tau als StringVar initialisieren
        self.entry = customtkinter.CTkEntry(self, textvariable=self.parent.tau)
        self.entry.grid(row=1, column=0, padx=10, pady=10)

        self.main_button_1 = customtkinter.CTkButton(
            self,
            fg_color="transparent",
            border_width=1,
            text="calc",
            text_color=("gray10", "#DCE4EE"),
            command=self.calc,
        )
        self.main_button_1.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Result label
        self.label = customtkinter.CTkLabel(self, width=200)
        self.label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.label.configure(text="Result: ")

    def change_scaling_event(self, new_scaling: str) -> None:
        """
        Adjusts the UI scaling factor for CustomTkinter widgets.
        """
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def calc(self) -> None:
        """
        Starts the main calculation.
        """
        entry_value = self.parent.tau.get()

        self.label.configure(text=f"Result: {logic(entry_value)}")
