# ControlPanel

## Overview
The `ControlPanel` class is a GUI component designed to provide various controls such as timescale input, buttons for minimizing chi-squared, calculating tau and absolute tau, and displaying results. It is implemented using `customtkinter` and is embedded in a parent GUI application.

## Class Definition
```python
class ControlPanel(customtkinter.CTkFrame):
```

## Initialization
### `__init__(self, parent: "App")`
Initializes the `ControlPanel` by creating a structured control interface with various widgets.

#### Parameters:
- `parent` (`App`): The parent application where the control panel is hosted.

## Methods


### `_create_timescale_widget()`

#### Description
The `_create_timescale_widget` method creates a timescale control widget that allows users to adjust the timescale value using a slider, an entry field, and buttons for fine adjustments. The widget also updates the calculated lifetime values based on the selected timescale.

#### Returns
- `customtkinter.CTkFrame`: A frame containing the timescale adjustment controls.

---

#### **Widget Components**
The method creates a `CTkFrame` containing:
1. **Update Button (`t [ps]`)**  
   - Triggers the `update_timescale` function to validate and apply the entered timescale value.
   
2. **Increment & Decrement Buttons (`+0.1[ps]`, `-0.1[ps]`)**  
   - Allows fine adjustment of the timescale by ±0.1 ps.

3. **Entry Field**  
   - Displays and allows direct input of the timescale value.

4. **Slider**  
   - Provides a graphical way to set the timescale within a valid range.

---

#### **Internal Functions**
##### `update_timescale()`
- Reads the value from the entry field and validates it.
- Updates the `timescale` variable if the value is within the allowed range (`0.01 - 100.0` ps).
- Calls `calculate_lifetime_for_custom_tau_factor` to compute the lifetime (`τ`) and its error (`Δτ`).
- Updates the displayed `τ` and `Δτ` values.
- Logs success or error messages.

##### `sync_slider(value)`
- Syncs the slider position with the entry field.
- Recalculates and updates the lifetime (`τ`) and error (`Δτ`).

##### `add_on_tau_factor(value)`
- Increases or decreases the timescale by `0.1` ps, ensuring it does not go below `0.0`.

---

#### **Layout Configuration**
- The frame uses a **grid layout** with **four columns**:
  - **Column 0:** "t [ps]" button
  - **Column 1:** "+0.1[ps]" button
  - **Column 2:** "-0.1[ps]" button
  - **Column 3:** Entry field (given more weight for a larger size)
- The slider spans all four columns.

---

#### **Usage**
This widget allows users to:
- Manually enter a timescale value.
- Adjust the timescale using buttons or a slider.
- View the updated `τ` and `Δτ` values in real-time.

---


### `_create_chi_squared_widget()
```python
def _create_chi_squared_widget(self) -> customtkinter.CTkFrame:
```
#### Description
Creates a widget displaying the chi-squared value and a button to minimize chi-squared.

#### Returns
- `customtkinter.CTkFrame`: A frame containing the chi-squared controls.

#### Functionality
- Displays a "Minimize" button that triggers chi-squared minimization.
- Shows the current chi-squared value in a label.

---

### `_create_tau_widget`

#### **Description**
The `_create_tau_widget` method creates a graphical widget for displaying the calculated lifetime (`τ`) and its associated error (`Δτ`). The widget also includes an absolute time difference (`|τ - t|`) display and a button for recalculating these values.

#### **Returns**
- `customtkinter.CTkFrame`: A frame containing all UI elements related to `τ` and `Δτ` values.

---

#### **Widget Components**
This method constructs a **main frame** with a **secondary frame** inside it:

##### **Main Frame (`CTkFrame`)**
1. **Button (`τ ± Δτ [ps]`)**
   - Calls `_tau_button_event(0.0, 0.0)` to update the values.

2. **Label (`|τ - t| [ps]:`)**
   - Displays the absolute difference between `τ` and `t`.

3. **Read-Only Entry (`|τ - t|` Value)**
   - Shows the absolute difference value stored in `self.result_absolute_tau_t`.

##### **Secondary Frame (`CTkFrame` within Main Frame)**
4. **Read-Only Entry (`τ` Value)**
   - Displays the calculated `τ`, retrieved from `self.result_tau`.

5. **Separator (`±`)**
   - Visually separates `τ` and `Δτ`.

6. **Read-Only Entry (`Δτ` Value)**
   - Displays the error `Δτ`, retrieved from `self.result_tau_error`.

---

#### **Internal Layout Configuration**
- The **main frame**:
  - Expands column `2` to ensure proper resizing.
  - Uses **grid layout** for structured positioning.

- The **secondary frame**:
  - Expands columns `0` and `2` for balanced spacing.
  - Also uses **grid layout**.

---


### `_create_absolute_tau_t_widget()`
```python
def _create_absolute_tau_t_widget(self) -> customtkinter.CTkFrame:
```
#### Description
Creates a widget for displaying the absolute difference between tau and t.

#### Returns
- `customtkinter.CTkFrame`: A frame containing absolute tau-related controls.

#### Functionality
- Includes a button labeled "Absolute τ" to trigger absolute tau calculation.
- Displays the calculated absolute tau value in a label.

---


### `_create_absolute_tau_t_widget(self) -> customtkinter.CTkFrame`
Creates a widget for displaying the absolute tau difference (`|τ - t|`).

#### Functionality:
- Displays `|τ - t|` value.
- Includes a button to trigger absolute tau calculation.

---

### `_timescale_button_event(self) -> None`
Handles events when the timescale button is clicked, printing the selected timescale value.

---

### `_timescale_slider_event(self, value: str) -> None`
Handles events when the timescale slider is moved. Set timescale value
to given value.

#### Parameters:
- `value` (`str`): The current value of the slider.

---

### `_tau_button_event(self) -> None`
Handles events when the tau calculation button is clicked.
Sets tau value to given value.


### `_chi_squared_button_event(self) -> None`
Handles events when the chi-squared button is clicked.
Sets chi-squared value to calculated value.

### `_absolute_tau_button_event(self) -> None`
Handles events when the absolute tau calculation button is clicked.
Sets the absolute tau value to calculated value.

### `set_result_chi_squared(self, chi_squared: float) -> None`
Sets the chi-squared result value.

#### Parameters:
- `chi_squared` (`float`): The new value for chi-squared.

---

### `set_result_tau(self, tau: float) -> None`
Sets the tau result value.

#### Parameters:
- `tau` (`float`): The new value for tau.

---

### `set_result_tau_error(self, tau_error: float) -> None`
Sets the tau error result value.

#### Parameters:
- `tau_error` (`float`): The new value for tau error.

---

### `set_result_absolute_tau_t(self, absolute_tau_t: float) -> None`
Sets the absolute tau result value.

#### Parameters:
- `absolute_tau_t` (`float`): The new value for absolute tau.

## Dependencies
- `customtkinter`: Used for creating UI elements.
- `napytau.gui.model.log_message_type.LogMessageType`: Used for logging messages.
- `napytau.gui.app.App`: The parent application where the control panel is embedded.


```

