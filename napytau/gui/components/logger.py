import customtkinter

from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.

class Logger(customtkinter.CTkFrame):
    def __init__(self, parent: "App") -> None:
        """
        Initializes the logger frame.
        :param parent: Parent widget to host the logger.
        """
        super().__init__(parent, height=10, corner_radius=10)
        self.parent = parent

        self.grid(row=2, column=0, columnspan=1, padx=(10, 10), pady=(10, 10),
                  sticky="ew")
        self.grid_propagate(False)

        # Create a scrollable frame for the log messages
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, height=40)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Set initial text colors
        if customtkinter.get_appearance_mode() == "Light":
            self.info_color = "black"
        else:
            self.info_color = "white"

        # Store labels in a deque with a max length of 50
        self.labels: deque = deque(maxlen=50)

    def log_info(self, message: str) -> None:
        """
        Appends an informational message to the logger.
        :param message: The message to log.
        """
        self._log_message("[INFO] " + message, color=self.info_color)

    def log_error(self, message: str) -> None:
        """
        Appends an error message to the logger in red.
        :param message: The error message to log.
        """
        self._log_message("[ERROR] " + message, color="red")

    def log_success(self, message: str) -> None:
        """
        Appends a success message to the logger.
        :param message: The message to log.
        """
        self._log_message("[SUCCESS] " + message, color="green")

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

        # Add the label to the deque
        self.labels.append(message_label)

        # Remove the oldest widget if the deque is full
        if len(self.labels) == self.labels.maxlen:
            oldest_label = self.labels.popleft()
            oldest_label.destroy()

        # Automatically scroll to the bottom
        self.scrollable_frame.update_idletasks()
        canvas = self.scrollable_frame._parent_canvas
        canvas.yview_scroll(canvas.bbox("all")[3], "units")

    def change_appearance_mode(self, appearance_mode: str) -> None:
        """
        Called when the appearance mode (light/dark) changes.
        Updates the text color of all labels accordingly.
        """
        if appearance_mode == "dark":
            self.info_color = "white"
        else:
            self.info_color = "black"

        # Update the text color for each label based on the appearance mode
        for label in self.labels:
            if label.cget("text").startswith("[INFO]"):
                if appearance_mode == "dark":
                    label.configure(text_color="white")
                else:
                    label.configure(text_color="black")
