#  Class: Toolbar

`CustomToolbar` extends the `NavigationToolbar2Tk` class from `matplotlib`, providing a customized toolbar with specific functionality for Napytau. This includes altering button styles, adjusting background colors, and removing unnecessary toolbar elements.

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

