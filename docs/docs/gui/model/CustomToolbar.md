# Custom Toolbar

## Overview



The original Toolbar module, provided by `customtkinter`, is not appropriate 
for napytau which is why we created our own custom Toolbar.

This Toolbar takes the original module from `customtkinter` and slightly adjusts it
to fit our needs.

## Initialization

Initializes the CustomToolbar object, by first creating an original customtkinter
toolbar and then setting it's color and font parameters.

After that certain buttons in the Toolbar are customized and buttons
present in the original toolbar, not needed for napytau, are removed.


## Attributes
None

## Methods

#### `__init__(self, canvas: FigureCanvasTkAgg, window: Frame, parent: "App") -> None`

##### Parameter:
- `canvas: FigureCanvasTkAgg`:   The `matplotlib` canvas widget used for rendering figures within the GUI.
- `window: Frame`: The parent frame in which the Toolbar is placed
- `parent: App`: The main application window

### Type Checking
The following import is used to ensure that type checking is correctly enforced:

```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from napytau.gui.app import App
```


This ensures that type annotations in the Toolbar and CustomToolbar classes reference the App class correctly without causing circular imports during runtime.
