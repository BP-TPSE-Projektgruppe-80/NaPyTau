from tkinter import Canvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import customtkinter
from typing import TYPE_CHECKING
import numpy as np

from napytau.gui.model.color import Color
from napytau.import_export.model.datapoint import Datapoint

from napytau.gui.model.marker_factory import generate_marker
from napytau.gui.model.marker_factory import generate_error_marker_path


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
        Is called whenever the graph needs to be re-rendered.
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
        shifted_intensities: list[float] = []
        shifted_intensity_errors: list[float] = []
        distances: list[float] = []

        shifted_intensities_fit: list[float] = []
        distances_fit: list[float] = []

        for datapoint in self.parent.datapoints_for_fitting:

            shifted_intensities.append(datapoint.get_shifted_intensity_value())
            distances.append(datapoint.get_distance_value())
            shifted_intensity_errors.append(datapoint.get_shifted_intensity_error())

            #Filtering Data from checked checkboxes
            if datapoint.is_checked:
                shifted_intensities_fit.append(datapoint.get_shifted_intensity_value())
                distances_fit.append(datapoint.get_distance_value())


        # the figure that will contain the plot
        fig = Figure(
            figsize=(3, 2),
            dpi=100,
            facecolor=Color.WHITE,
            edgecolor=Color.BLACK
        )

        # adding the subplot
        axes_1 = fig.add_subplot(111)
        fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)

        # set colors according to appearance mode
        self.set_colors(appearance)

        # apply colors onto figure and axes
        self.apply_coloring(fig, axes_1)

        # add grid style
        axes_1.grid(
            True,
            which="both",
            color=self.secondary_color,
            linestyle="--",
            linewidth=0.3
        )

        # draw the markers on the axes
        self.plot_markers(
            distances,
            shifted_intensities,
            shifted_intensity_errors,
            axes_1
        )

        # draw the fitting curve on the axes
        self.plot_fitting_curve(
            distances_fit,
            shifted_intensities_fit,
            axes_1)


        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(fig, master=self.parent)
        self.canvas.draw()

        return self.canvas.get_tk_widget()

    def set_colors(self, appearance: str) -> None:

        if appearance == "Light":
            self.main_color = Color.WHITE
            self.secondary_color = Color.BLACK
            self.main_marker_color = Color.DARK_GREEN

        else:
            self.main_color = Color.DARK_GRAY
            self.secondary_color = Color.WHITE
            self.main_marker_color = Color.LIGHT_GREEN



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
                     distances: list,
                     shifted_intensities: list,
                     shifted_intensity_errors: list,

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
        for index in range(len(shifted_intensities)):
            # Generate marker and compute dynamic markersize
            marker = generate_marker(generate_error_marker_path(shifted_intensity_errors[index]))
            size = shifted_intensity_errors[index] * 5  # Scale markersize based on distance
            axes.plot(
                distances[index],
                shifted_intensities[index],
                marker=marker,
                linestyle="None",
                markersize=size,
                label=f"Point {index + 1}",
                color=self.main_marker_color,
            )
    def plot_fitting_curve(self, distances_fit: list, shifted_intensities_fit: list, axes: Axes)-> None:

        """
         plotting fitting curve of datapoints
        :param x_data: x coordinates
        :param y_data: y coordinates
        :param axes: the axes on which to draw the fitting curve
        :return: nothing
        """

        # Calculating coefficients
        coeffs = np.polyfit(distances_fit, shifted_intensities_fit, len(shifted_intensities_fit))

        poly = np.poly1d(coeffs)  # Creating polynomial with given coefficients

        x_fit = np.linspace(min(distances_fit), max(distances_fit), 100)
        y_fit = poly(x_fit)

        #plot the curve
        axes.plot(
            x_fit, y_fit, color="red", linestyle="--", linewidth="0.6"
        )





