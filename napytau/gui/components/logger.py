import customtkinter

from collections import deque
from typing import TYPE_CHECKING
from napytau.gui.model.color import Color

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.

from enum import Enum

class MessageType(Enum):
    INFO = "[INFO]"
    ERROR = "[ERROR]"
    SUCCESS = "[SUCCESS]"

class Logger(customtkinter.CTkFrame):
    def __init__(self, parent: "App") -> None:
        """
        A scrolling textbox, displaying up to 50 queued messages.
        :param parent: Parent widget to host the logger.
        """
        super().__init__(parent, height=10, corner_radius=10)
        self.parent = parent

        self.grid(row=2, column=0, columnspan=1, padx=(10, 10), pady=(10, 10),
                  sticky="ew")
        self.grid_propagate(False)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, height=40)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Set initial text colors
        if customtkinter.get_appearance_mode() == "Light":
            self.info_color = Color.LIGHT_MODE_INFO_COLOR
            self.error_color = Color.LIGHT_MODE_ERROR_COLOR
            self.success_color = Color.LIGHT_MODE_SUCCESS_COLOR
        else:
            self.info_color = Color.DARK_MODE_INFO_COLOR
            self.error_color = Color.DARK_MODE_ERROR_COLOR
            self.success_color = Color.DARK_MODE_SUCCESS_COLOR

        self.labels: deque = deque(maxlen=50)

    def log_message(self, message: str, message_type: MessageType) -> None:
        """
        Adds a message to the logger. Scrolls down to the bottom of the logger frame.
        :param message_type: The message type.
        :param message: The message to append.
        """
        color: str
        if message_type == MessageType.ERROR:
            color = self.error_color
        elif message_type == MessageType.SUCCESS:
            color = self.success_color
        else:
            color = self.info_color

        message_label = customtkinter.CTkLabel(
            self.scrollable_frame,
            text=message_type.value + " " + message,
            fg_color="transparent",
            text_color=color,
            anchor="w"
        )
        message_label.pack(fill="x", padx=5, pady=0)

        self.labels.append(message_label)

        # Remove the oldest widget if the deque is full
        if len(self.labels) == self.labels.maxlen:
            oldest_label = self.labels.popleft()
            oldest_label.destroy()

        # Automatically scroll to the bottom
        self.scrollable_frame.update_idletasks()
        canvas = self.scrollable_frame._parent_canvas
        canvas.yview_scroll(canvas.bbox("all")[3], "units")

    def switch_logger_appearance(self, appearance_mode: str) -> None:
        """
        Called when the appearance mode (light/dark) changes.
        Updates the text color of all labels accordingly.
        :param appearance_mode: The appearance mode to change to.
        """
        if appearance_mode == "dark":
            self.info_color = Color.DARK_MODE_INFO_COLOR
            self.error_color = Color.DARK_MODE_ERROR_COLOR
            self.success_color = Color.DARK_MODE_SUCCESS_COLOR
        else:
            self.info_color = Color.LIGHT_MODE_INFO_COLOR
            self.error_color = Color.LIGHT_MODE_ERROR_COLOR
            self.success_color = Color.LIGHT_MODE_SUCCESS_COLOR

        # Update the text color for each label based on the appearance mode
        for label in self.labels:
            if label.cget("text").startswith("[ERROR]"):
                label.configure(text_color=self.error_color)
            elif label.cget("text").startswith("[SUCCESS]"):
                label.configure(text_color=self.success_color)
            else:
                label.configure(text_color=self.info_color)
