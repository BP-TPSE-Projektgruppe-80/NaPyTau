# Logger Class

The `Logger` class provides a scrolling text box for displaying log messages with different message types, including informational, error, and success messages. It is designed to store and display up to 50 messages at a time.

## Attributes

- **`parent`** (`App`): The parent widget that contains the logger.
- **`scrollable_frame`** (`customtkinter.CTkScrollableFrame`): A scrollable frame that holds the log messages.
- **`info_color`** (`str`): The color used for informational messages.
- **`error_color`** (`str`): The color used for error messages.
- **`success_color`** (`str`): The color used for success messages.
- **`labels`** (`deque`): A deque (double-ended queue) storing the last 50 log messages for efficient management.

## Methods

### `__init__`

Initializes the `Logger` widget.

#### Parameters
- **`parent`**: The parent widget where the logger will be placed.

#### Description
- Creates a frame with a scrollable area for log messages.
- Initializes text colors based on the current appearance mode (light or dark).
- Stores messages in a `deque` for efficient message handling.

---

### `log_message`

Logs a new message in the logger frame and scrolls to the most recent message.

#### Parameters
- **`message`**: The text message to be logged.
- **`message_type`**: The type of message (INFO, ERROR, SUCCESS).

#### Description
- Determines the text color based on the message type.
- Creates a label inside the scrollable frame for the message.
- Stores the message in a deque (removing the oldest message if the limit of 50 is reached).
- Scrolls to the most recent message.

---

### `switch_logger_appearance(self, appearance_mode: str) -> None`

Updates the text colors of log messages when the appearance mode (light/dark) changes.

#### Parameters
- **`appearance_mode`** (`str`): The new appearance mode ("light" or "dark").

#### Description
- Updates the logger's color scheme based on the selected mode.
- Adjusts the text color of all existing log messages accordingly.
