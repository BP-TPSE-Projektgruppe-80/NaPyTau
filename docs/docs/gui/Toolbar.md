# Class: Toolbar

The 'Toolbar' class is responsible for creating and managing a toolbar widget within a `tkinter` application. It integrates the `CustomToolbar` class for custom toolbar functionality. It is primarily used in conjunction with a `matplotlib` figure, where the toolbar interacts with the figure's canvas to provide custom controls.

## Attributes
None


## Methods

#### `__init__(self, parent: "App", canvas: FigureCanvasTkAgg) -> None`

##### Parameters:
- `parent: App`:
 The parent application which holds the main graphical interface
- `canvas: FigureCanvasTkAgg`:
 The `matplotlib` canvas widget used for rendering figures within the GUI.

##### Description:
The constructor initializes the toolbar by:

1. Create a `tk.Frame` to contain the toolbar
2. Setting the background color depending on appearance mode
3. Adding a `CustomToolbar`instance to the Frame, which provides the functionality
4. Calling the `update()` method on the `CustomToolbar` instance to refresh the toolbar

##### Description:

The constructor customizes the toolbar by:

1. Calling the parent class constructor (`NavigationToolbar2Tk`) to initialize the default toolbar functionality.
2. Customizing the message label's appearance, including background and foreground colors and font settings, based on the parent application's color scheme.
3. Iterating over the toolbar's items (buttons) and modifying their appearance. This includes changing the background color of each button to green, setting a flat relief style, and disabling the highlight thickness.
4. Removing unnecessary buttons from the toolbar by destroying specific child widgets that are not needed for the application.


### Type Checking
The following import is used to ensure that type checking is correctly enforced:

```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from napytau.gui.app import App
```


This ensures that type annotations in the Toolbar and CustomToolbar classes reference the App class correctly without causing circular imports during runtime.
