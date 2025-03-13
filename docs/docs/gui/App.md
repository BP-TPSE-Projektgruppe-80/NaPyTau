# App

## Overview

The "App" Class is an extension of the customtkinter.Ctk class and as such represents the main window of the application, containing all GUI Components in an ordered Grid. 

When Napytau is started and the entry point is executed in Gui-Mode, initializing an instance of the App Class is the first and only thing it will do.

When initialized the App will sequentially call the constructors off all needed GUI-Components and build the Application.



## Attributes

### Datapoint Collections (Managing Data)

#### `datapoints`
Stores all loaded datapoints used in the application.

#### `datapoints_for_fitting`
Stores datapoints which should specifically be used for fitting calculations.

#### `datapoints_for_calculation`
Stores datapoints that should be used when doing general calculations.

---

### Tkinter Variables

##### `tau`

Variable dynamically containing the latest result of the tau calculation. 

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

#### `checkbox_panel`
Creates a **Checkbox Panel** for selecting data points interactively.

#### `update_data_checkboxes`
Updates the datapoint for the gui and updates both columns of the data checkboxes.
Call this method if there are new datapoints.

---

### Graph (Plotting Data)

#### `graph`
Initializes a **Graph Component** for visualizing data in a plot.

---

### Toolbar (Graph Controls)

#### `toolbar`
Creates a **Toolbar** to allow users to interact with the graph (zoom, pan, reset, etc.).

---

### Control Panel (User Inputs)

#### `control_panel`
Initializes a **Control Panel** for adjusting parameters and user inputs.

---

### Logger (Message Logging)

#### `logger`
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




### `open_file`
Opens the file explorer and allows the user to choose a file.
Logs the chosen file path.

### `save_file`
Saves the file and logs a success message.

### `read_setup`
Reads the setup and logs a message (currently not implemented).

### `quit`
Closes the application.

### `change_appearance_mode`
Changes the application's appearance mode and updates the logger appearance.

### `select_number_of_polynomials`
Logs the selected number of polynomials (currently not implemented).

### `select_polynomial_mode`
Logs the selected polynomial mode (currently not implemented).

### `select_alpha_calc_mode`
Logs the selected alpha calculation mode (currently not implemented).

### `update_data_checkboxes`
Updates the datapoint collection for the GUI and refreshes the checkbox panels.

---

## **Table of Main Functions**

| **Method** | **Purpose** |
|----------------------|------------|
| `open_file()`, `save_file()`, `read_file` | Handles file operations. |
| `change_appearance_mode()` | Updates the application's appearance mode. |
| `select_number_of_polynomials()`, `select_polynomial_mode()`, `select_alpha_calc_mode()` | Logs selections for various settings. |
| `update_data_checkboxes(new_datapoints)` | Updates GUI data checkboxes with new datapoints. |

---

