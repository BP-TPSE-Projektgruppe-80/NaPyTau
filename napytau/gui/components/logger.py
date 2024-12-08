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
        super().__init__(parent, height=50, corner_radius=10)
        self.parent = parent
        self.grid_propagate(False)
        self.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="nsew")

        # Create a scrollable frame for the log messages
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def log_info(self, message: str) -> None:
        """
        Appends an informational message to the logger.
        :param message: The message to log.
        """
        self._log_message(message, color="black")

    def log_error(self, message: str) -> None:
        """
        Appends an error message to the logger in red.
        :param message: The error message to log.
        """
        self._log_message(message, color="red")

    def log_success(self, message: str) -> None:
        """
        Appends a success message to the logger.
        :param message: The message to log.
        """
        self._log_message(message, color="green")

    def _log_message(self, message: str, color: str) -> None:
        """
        Adds a message to the scrollable frame as a label.
        :param message: The message to append.
        :param color: The color of the text.
        """
        # Create a new label for the message
        message_label = customtkinter.CTkLabel(
            self.scrollable_frame,
            text=message,
            fg_color="transparent",
            text_color=color,
            anchor="w"
        )
        message_label.pack(fill="x", padx=5, pady=0)

        # Automatically scroll to the bottom
        self.scrollable_frame.update_idletasks()
        canvas = self.scrollable_frame._parent_canvas
        canvas.yview_scroll(canvas.bbox("all")[3], "units")