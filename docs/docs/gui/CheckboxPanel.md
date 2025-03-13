
# CheckboxPanel

## Overview
The `CheckboxPanel` class is responsible for 
managing a panel of checkboxes used to select 
data points for fitting and calculations. It is 
implemented using `customtkinter` and is embedded 
in a parent GUI application.

## Class Definition
```python
class CheckboxPanel:
```

## Initialization
### `__init__(self, parent: "App") -> None`
Initializes the `CheckboxPanel` by creating a scrollable frame to host the checkboxes.

#### Parameters:
- `parent` (`App`): The parent application where the panel is hosted.

## Methods

### `update_data_checkboxes_fitting(self) -> None`
Updates the checkboxes corresponding to data 
points available for fitting. This method 
clears any existing checkboxes and repopulates 
them with the latest data points.


### `_data_checkbox_fitting_event(self, index: int) -> None`
Handles checkbox state changes for fitting data points. 

#### Parameters:
- `index` (`int`): The index of the selected data checkbox.

#### Discription
When pressing a checkbox:
- The active state of the corresponding data point is toggled.
- Activation or deactivation of the checkbox is logged.
- Graph is updated.

---

### `update_data_checkboxes_calculation(self) -> None`
Updates the checkboxes corresponding to data 
points used for calculating **tau** and **delta-tau**. 
This method clears old checkboxes and adds new ones. 
This method is currently not actively used in the napytau version, since
checkboxes for datapoint calculations are not currently implemented.

#### Discription:
- Removes existing checkboxes in column 1.
- Adds a header label: **"Tau calculation"**.
- Creates and places checkboxes for each data point.
- Each checkbox toggles the active state of a datapoint when clicked.

---

### `_data_checkbox_calculation_event(self, index: int) -> None`
Handles checkbox state changes for data points used in tau calculations.

#### Parameters:
- `index` (`int`): The index of the selected data checkbox.

#### Discription:

When pressed:
- Toggles the active state of the corresponding data point.
- Logs activation or deactivation of the checkbox.

## Dependencies
- `customtkinter`: Used for creating UI elements.
- `napytau.gui.model.log_message_type.LogMessageType`: Used for logging messages.
- `napytau.gui.app.App`: The parent application where the checkbox panel is embedded.

## Notes
- The `_data_checkbox_fitting_event` and `_data_checkbox_calculation_event` methods should not be called externally.
- This class dynamically updates its UI elements based on the data points available in `self.parent.datapoints`.

## Example Usage
```python
parent_app = App()
checkbox_panel = CheckboxPanel(parent_app)
checkbox_panel.update_data_checkboxes_fitting(<Random Datapoint>)
checkbox_panel.update_data_checkboxes_calculation(<Random Datapoint>)
```
This will create a `CheckboxPanel`, attach it to the `parent_app`, and update checkboxes for both fitting and calculation.

