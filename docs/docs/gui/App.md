# Class: App

## General
The "App" Class is an extension of the customtkinter.Ctk class and as such represents the main window of the application, containing all GUI Components in an ordered Grid. 

When Napytau is started and the [napytau/main.py] is executed in Gui-Mode, initializing an instance of the App Class is the first and only thing it will do.

When initialized the App will systematically call the constructors off all needed GUI-Components and build the Application.

## Attributes

### Datapoint Collections (Managing Data)

#### `datapoints: DatapointCollection`
Stores all loaded datapoints used in the application.

#### `datapoints_for_fitting: DatapointCollection`
Stores datapoints specifically used for fitting calculations.

#### `datapoints_for_calculation: DatapointCollection`
Stores datapoints that will be used for general calculations.

---

### Tkinter Variables

##### `tau: tk.IntVar`
A Tkinter integer variable initialized to `2`. Used to store and manage an integer value dynamically in the UI.

---

### Window Configuration

#### `title("NaPyTau")`
Sets the application window title to "NaPyTau".

#### `geometry(f"{width}x{height}")`
Defines the application window size as `1366x768` pixels.

---

### Grid Layout Configuration (GUI Layout)

#### `grid_rowconfigure`
Defines the row height proportions for the layout:
- **Row 0:** Weight = 3, minimum size = `3 * height // total_height`
- **Row 1:** Weight = 3, minimum size = `3 * height // total_height - 30`
- **Row 2:** Weight = 2, minimum size = `2 * height // total_height`

#### `grid_columnconfigure`
Defines the column width proportions:
- **Column 0:** Weight = 2, minimum size = `3 * width // total_width - 30`
- **Column 1:** Weight = 1, minimum size = `1 * width // total_width`

---

### Menu Bar (Navigation & Settings)

#### `menu_bar: MenuBar`
Initializes a **Menu Bar** component with callback functions for:
- Opening/Saving files
- Quitting the application
- Changing themes and settings

---

### Checkbox Panel (Data Selection)

#### `checkbox_panel: CheckboxPanel`
Creates a **Checkbox Panel** for selecting data points interactively.

#### `update_data_checkboxes([...])`
Populates the checkboxes with sample (dummy) datapoints for testing purposes.

---

### Graph (Plotting Data)

#### `graph: Graph`
Initializes a **Graph Component** for visualizing data through plots.

---

### Toolbar (Graph Controls)

#### `toolbar: Toolbar`
Creates a **Toolbar** to allow users to interact with the graph (zoom, pan, reset, etc.).

---

### Control Panel (User Inputs)

#### `control_panel: ControlPanel`
Initializes a **Control Panel** for adjusting parameters and user inputs.

---

### Logger (Message Logging)

#### `logger: Logger`
Creates a **Logger Component** to display system messages, errors, and logs to the user.

---

## **Table of Main Attributes**

| **Attribute** | **Purpose** |
|--------------|------------|
| `datapoints`, `datapoints_for_fitting`, `datapoints_for_calculation` | Stores and manages datapoint collections. |
| `tau` | Stores a numerical value (Tkinter variable). |
| `menu_bar` | Handles file operations and settings. |
| `checkbox_panel` | Allows users to select datapoints. |
| `graph`, `toolbar` | Displays and interacts with plotted data. |
| `control_panel` | Manages user controls and configurations. |
| `logger` | Displays logs, messages, and status updates. |

---



## Methods




### `open_file() -> None`
Opens the file explorer and allows the user to choose a file.
Logs the chosen file path.

### `save_file() -> None`
Saves the file and logs a success message.

### `read_setup() -> None`
Reads the setup and logs a message (currently not implemented).

### `quit() -> None`
Closes the application.

### `change_appearance_mode() -> None`
Changes the application's appearance mode and updates the logger appearance.

### `select_number_of_polynomials() -> None`
Logs the selected number of polynomials (currently not implemented).

### `select_polynomial_mode() -> None`
Logs the selected polynomial mode (currently not implemented).

### `select_alpha_calc_mode() -> None`
Logs the selected alpha calculation mode (currently not implemented).

### `update_data_checkboxes(new_datapoints: List[Datapoint]) -> None`
Updates the datapoint collection for the GUI and refreshes the checkbox panels.

---

## **Table of Main Functions Areas**

| **Method** | **Purpose** |
|----------------------|------------|
| `open_file()`, `save_file()`, `read_file` | Handles file operations. |
| `change_appearance_mode()` | Updates the application's appearance mode. |
| `select_number_of_polynomials()`, `select_polynomial_mode()`, `select_alpha_calc_mode()` | Logs selections for various settings. |
| `update_data_checkboxes(new_datapoints)` | Updates GUI data checkboxes with new datapoints. |

---

