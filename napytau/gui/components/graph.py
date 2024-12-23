from tkinter import Canvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.path import Path
from matplotlib.markers import MarkerStyle
from matplotlib.axes import Axes
import customtkinter
from typing import TYPE_CHECKING
import numpy as np

from napytau.gui.model.color import Color



if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.


class Graph:

    def __init__(self, parent: "App") -> None:

        self.parent = parent
        self.graph_frame = self.plot(
             customtkinter.get_appearance_mode()
        )
        self.graph_frame.grid(
            row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew"
        )
        self.graph_frame.grid_propagate(False)

    def update_plot(self) -> None:
        """
        Is called whenever changes on the graphs appearance should occur.
        """
        self.graph_frame = self.plot(
             customtkinter.get_appearance_mode()
        )
        self.graph_frame.grid(
            row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew"
        )
        self.graph_frame.grid_propagate(False)

    def plot(self, appearance: str) -> Canvas:


        #Extracting Data:
        y_data = []
        x_data = []

        y_data_fit = []
        x_data_fit = []

        for datapoint in self.parent.datapoints_for_fitting:

            y_data.append(datapoint.coordinates[1])
            x_data.append(datapoint.coordinates[0])

            #Filtering Data from checked checkboxes
            if datapoint.is_checked:
                y_data_fit.append(datapoint.coordinates[1])
                x_data_fit.append(datapoint.coordinates[0])

        #Placeholder Data:

        distances = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10
        ]


        # the figure that will contain the plot
        fig = Figure(
            figsize=(3, 2),
            dpi=100,
            facecolor=Color.WHITE,
            edgecolor=Color.BLACK
        )

        # adding the subplot
        Axes_1 = fig.add_subplot(111)

        # set colors according to appearance mode
        self.set_colors(appearance)

        # apply colors onto figure and axes
        self.apply_coloring(fig, Axes_1)

        # add grid style
        Axes_1.grid(
            True,
            which="both",
            color=self.secondary_color,
            linestyle="--",
            linewidth=0.3
        )

        # draw the markers on the axes
        self.plot_markers(
            x_data,
            y_data,
            distances,
            Axes_1
        )

        # draw the fitting curve on the axes
        self.plot_fitting_curve(
            x_data_fit,
            y_data_fit,
            Axes_1)


        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.parent)
        canvas.draw()

        return canvas.get_tk_widget()

    def set_colors(self, appearance: str) -> None:

        if appearance == "Light":
            self.main_color = Color.WHITE
            self.secondary_color = Color.BLACK
            self.main_marker_color = Color.DARK_GREEN
            #.
            #.
            #.
        else:
            self.main_color = Color.DARK_GRAY
            self.secondary_color = Color.WHITE
            self.main_marker_color = Color.LIGHT_GREEN
            #.
            #.
            #.


    def apply_coloring(self, figure: Figure, axes: Axes) -> None:
        """
        setting color in dependence of appearance mode
        :param figure: the figure to be recolored
        :param axes: the axes to be recolored
        :return: nothing
        """

        figure.patch.set_facecolor(self.main_color)

        # set color of background
        axes.set_facecolor(self.main_color)

        # set color of ticks
        axes.tick_params(axis="x", colors=self.secondary_color)
        axes.tick_params(axis="y", colors=self.secondary_color)

    def plot_markers(self,
                     x_data: list,
                     y_data: list,
                     distances: list,
                     axes: Axes
                     ) -> None:
        """
        plotting the datapoints with appropriate markers
        :param x_data: x coordinates
        :param y_data: y coordinates
        :param distances: error amount of datapoint -> needed to configure marker length
        :param axes: the axes on which to draw the markers
        :return: nothing
        """
        for index in range(len(y_data)):
            # Generate marker and compute dynamic markersize
            marker = generate_marker(generate_error_marker_path(distances[index]))
            size = distances[index] * 5  # Scale markersize based on distance
            axes.plot(
                x_data[index],
                y_data[index],
                marker=marker,
                linestyle="None",
                markersize=size,
                label=f"Point {index + 1}",
                color=self.main_marker_color,
            )
    def plot_fitting_curve(self, x_data_fit: list, y_data_fit: list, axes: Axes)-> None:

        """
         plotting fitting curve of datapoints
        :param x_data: x coordinates
        :param y_data: y coordinates
        :param axes: the axes on which to draw the fitting curve
        :return: nothing
        """

        # Calculating coefficients
        coeffs = np.polyfit(x_data_fit, y_data_fit, len(y_data_fit))

        poly = np.poly1d(coeffs)  # Creating polynomial with given coefficients

        x_fit = np.linspace(min(x_data_fit), max(x_data_fit), 100)
        y_fit = poly(x_fit)

        #plot the curve
        axes.plot(
            x_fit, y_fit, color="red", linestyle="--", linewidth="0.6"
        )


def generate_error_marker_path(error_amount: float) -> Path:

    """
    Create a path to describe how an error marker should be drawn around a data point
    """

    y_coord = error_amount / 2   #marker shape length depends on error amount

    verts = [               #Defines coordinates for the markers shape like this:
        (-0.5, y_coord),    #        *--*--*        (-0.5, y)---(0, y)---(0.5, y)
        (0.5, y_coord),     #           |                          |
        (0, y_coord),       #           |                        (0,0)
        (0, -y_coord),      #           |                          |
        (-0.5, -y_coord),   #        *--*--*       (-0.5, -y)---(0, -y)---(0.5, -y)
        (0.5, -y_coord),
    ]

    """
    After defining coordinates of the shape we need instruction on how to connect 
    each point which each other to create the desired marker shape
    """

    instructions = [
        Path.MOVETO,        #Move "pen" to point (first coord in 'verts' -> (-0.5, -y))
        Path.LINETO,        #Draw line towards second coord in 'verts' (0.5, -y)
        Path.MOVETO,        #Move "pen" to third point in 'verts'
        Path.LINETO,        #Draw line to fourth point in 'verts'
        Path.MOVETO,        #Move pen....
        Path.LINETO,        #Draw...
    ]

    return Path(verts, instructions)



def generate_marker(path: Path) -> MarkerStyle:
    """Creates new marker for the given path."""
    return MarkerStyle(path)


