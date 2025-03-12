# Custom Toolbar

The original Toolbar module, provided by `customtkinter`, is not appropriate 
for napytau which is why we created our own custom Toolbar.

This Toolbar takes the original module from customtkinter and slightly bends it
to fit our needs.

## Initialization

### `__init__(self, canvas: FigureCanvasTkAgg, window: Frame, parent: "App") -> None:`
Initializes the CustomToolbar object, by first creating an original customtkinter
toolbar and then setting it's color and font parameters.

After that certain buttons in the Toolbar are customized and button
present in the original toolbar, not needed for napytau, are removed.