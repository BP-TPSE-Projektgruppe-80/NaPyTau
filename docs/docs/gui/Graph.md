# Graph

## Overview

The `Graph` class is responsible for rendering and updating a graphical representation of `datapoints` in the NaPyTau application. It utilizes `matplotlib` to create plots and integrates with `tkinter` via `FigureCanvasTkAgg`.

When constructed the `App` instance will give itself as a parent to the Graph. The Graph component can access the needed datapoints and other Attributes from this parent reference.

The `Graph` class is used within the `App` to render data visualizations. It updates dynamically based on user interactions and selected appearance modes.



## Attributes

#### `parent`
Reference to the parent application instance.

#### `graph_frame`
The main canvas widget where the graph is displayed.

#### `canvas`
A tkinter-compatible Matplotlib figure canvas containing the graph.

#### `main_color`
The primary background color for the graph, adapting to appearance mode.

#### `secondary_color`
The secondary color used for elements like grid lines and ticks.

#### `main_marker_color`
The primary color used for markers on the graph.

#### `secondary_marker_color`
The secondary color used for markers on the graph.

---

### Table of Attributes

| Attribute                  |Description                                         |
|----------------------------|------------------------|
| `parent`                   | Reference to the parent application instance.             |
| `graph_frame`              | The main canvas widget where the graph is displayed.      |
| `canvas`                   | A tkinter-compatible Matplotlib figure canvas containing the graph. |
| `main_color`, `secondary_color`, `main_marker_color`, `secondary_marker_color`               | Attributes used for coloring

---

## Methods


#### `plot`
- **Description**: Creates and configures the Matplotlib figure and axes based on the provided appearance mode.
- **Returns**: `Canvas` widget containing the plotted figure.

#### `update_plot`
- **Description**: Re-renders the graph and updates the toolbar.

#### `set_colors`
- **Description**: Adjusts color settings based on the current appearance mode.

#### `apply_coloring`
- **Description**: Applies the selected color scheme to the figure and axes.

#### `plot_markers`
- **Description**: Plots data points with appropriate markers based on their error values.

#### `plot_fitting_curve`
- **Description**: Generates and plots a polynomial fitting curve for the selected data points.

#### `plot_derivative_curve
- **Description**: Generates and plots the derivative of the polynomial fitting curve for the selected data points.




