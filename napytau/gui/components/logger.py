import customtkinter

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.

class Logger(customtkinter.CTkFrame):
    def __init__(self, parent: "App") -> None:
        """
        Initializes the logger frame.
        :param parent: Parent widget to host the logger.
        """
        super().__init__(parent, height=100, corner_radius=10)
        self.parent = parent
        self.grid_propagate(False)
        self.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Label to display messages
        self.output_label = customtkinter.CTkLabel(
            self, text="Error messages etc. will be shown here", anchor="w")
        self.output_label.pack(fill="both", padx=10, pady=10)