from tkinter import Canvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.path import Path
from matplotlib.markers import MarkerStyle
import customtkinter
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.

class Graph:
    def __init__(self, parent: "App") -> None:
        """
        Initializes the graph.
        :param parent: Parent widget to host the graph.
        """
        self.parent = parent
        self.graph_frame = self.plot(
            self.parent.tau.get(), customtkinter.get_appearance_mode()
        )
        self.graph_frame.grid(
            row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew"
        )
        self.graph_frame.grid_propagate(False)

    def update_plot(self) -> None:
        """
        Updates the graph with the latest tau value and appearance mode.
        """
        self.graph_frame = self.plot(
            self.parent.tau.get(), customtkinter.get_appearance_mode()
        )
        self.graph_frame.grid(
            row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew"
        )
        self.graph_frame.grid_propagate(False)

    def plot(self, value: int, appearance: str) -> Canvas:
        """
        Plot the graph.
        :param appearance: The appearance mode.
        :param value: The value.
        :return: The canvas.
        """

        #Placeholder datapoints:
        y_data = [2, 4, 5, 7, 8, 9, 11, 15]
        distances = [1, 2, 3, 4, 5, 6, 7, 8]
        x_data = [0, 1, 2, 3, 4, 5, 6, 7]


        # the figure that will contain the plot
        fig = Figure(figsize=(3, 2), dpi=100, facecolor="white", edgecolor="black")

        # setting color in dependence of appearance mode
        if appearance == "Light":
            main_color = "white"
            secondary_color = "#000000"
            main_marker_color = 'g'
        else:
            main_color = "#151515"
            secondary_color = "#ffffff"
            main_marker_color = "#2eff2a"

        fig.patch.set_facecolor(main_color)



        # adding the subplot
        plot1 = fig.add_subplot(111)

        # set color of background
        plot1.set_facecolor(main_color)

        # set color of ticks
        plot1.tick_params(axis="x", colors=secondary_color)
        plot1.tick_params(axis="y", colors=secondary_color)

        # add grid style
        plot1.grid(
            True, which="both", color=secondary_color, linestyle="--", linewidth=0.3
        )

        # plotting the datapoints with appropriate markers
        for index in range(len(y_data)):
            # Generate marker and compute dynamic markersize
            marker = MarkerStyle(generate_marker(distances[index]))
            size = distances[index] * 5  # Scale markersize based on distance
            plot1.plot(
                x_data[index],
                y_data[index],
                marker=marker,
                linestyle='None',
                markersize=size,
                label=f"Point {index + 1}",
                color= main_marker_color
            )

        #plotting fitting curve of datapoints

        coeffs = np.polyfit(x_data, y_data, 10)  #Calculating coefficients

        poly = np.poly1d(coeffs)  #Creating polynomial with given coefficients

        x_fit = np.linspace(min(x_data), max(x_data), 100)
        y_fit = poly(x_fit)

        plot1.plot(x_fit, y_fit, color='red', linestyle="--", linewidth='0.6')  #plotting

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.parent)
        canvas.draw()

        return canvas.get_tk_widget()



# Generate custom marker function
def generate_marker(distance: float):
    #Instructions for creating marker design
    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.MOVETO,
        Path.LINETO,
        Path.MOVETO,
        Path.LINETO
    ]

    y_coord = distance / 2
    verts = [
        (-0.5, -y_coord),
        (0.5, -y_coord),
        (0, -y_coord),
        (0, y_coord),
        (-0.5, y_coord),
        (0.5, y_coord)
    ]
    return Path(verts, codes)