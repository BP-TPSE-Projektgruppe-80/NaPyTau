from tkinter import Canvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.axes import Axes
import customtkinter
from typing import TYPE_CHECKING
import numpy as np

from napytau.gui.components.toolbar import Toolbar
from napytau.gui.model.color import Color
from napytau.gui.model.marker_factory import generate_marker
from napytau.gui.model.marker_factory import generate_error_marker_path

from napytau.import_export.model.datapoint_collection import DatapointCollection


if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.


class Graph:
    def __init__(self, parent: "App") -> None:
        self.parent = parent
        self.graph_frame = self.plot(customtkinter.get_appearance_mode())
        self.graph_frame.grid(
            row=1, column=0, rowspan=2, padx=(10, 10), pady=(10, 0), sticky="nsew"
        )
        self.graph_frame.grid_propagate(False)

    def plot(self, appearance: str) -> Canvas:
        # the figure that will contain the plot
        fig = Figure(
            figsize=(3, 2), dpi=100, facecolor=Color.WHITE, edgecolor=Color.BLACK
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
            linewidth=0.3,
        )

        axes_1.set_xscale("log")

        # draw the markers on the axes
        self.plot_markers(self.parent.datapoints_for_fitting, axes_1)

        if len(self.parent.datapoints_for_fitting.get_active_datapoints()) > 0:
            # draw the fitting curve
            self.plot_fitting_curve(self.parent.datapoints_for_fitting, axes_1)
            self.plot_derivative_curve(self.parent.datapoints_for_fitting, axes_1)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(fig, master=self.parent)
        self.canvas.draw()

        return self.canvas.get_tk_widget()

    def update_plot(self) -> None:
        """
        Is called whenever the graph needs to be re-rendered.
        """
        self.graph_frame = self.plot(customtkinter.get_appearance_mode())
        self.graph_frame.grid(
            row=1, column=0, rowspan=2, padx=(10, 10), pady=(10, 0), sticky="nsew"
        )
        self.graph_frame.grid_propagate(False)
        self.parent.toolbar = Toolbar(self.parent, self.canvas)

    def set_colors(self, appearance: str) -> None:
        if appearance == "Light":
            self.main_color = Color.WHITE
            self.secondary_color = Color.BLACK
            self.main_marker_color = Color.DARK_GREEN
            self.secondary_marker_color = Color.DARK_RED

        else:
            self.main_color = Color.DARK_GRAY
            self.secondary_color = Color.WHITE
            self.main_marker_color = Color.LIGHT_GREEN
            self.secondary_marker_color = Color.Light_RED

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

    def plot_markers(self, datapoints: DatapointCollection, axes: Axes) -> None:
        """
        plotting the datapoints with appropriate markers
        :param x_data: x coordinates
        :param y_data: y coordinates
        :param distances: error amount of datapoint -> needed to configure marker length
        :param axes: the axes on which to draw the markers
        :return: nothing
        """
        # Extracting distance values / intensities of checked datapoints
        checked_datapoints: DatapointCollection = datapoints.get_active_datapoints()

        index: int = 0
        for datapoint in checked_datapoints:
            # Generate marker and compute dynamic markersize
            marker_shifted = generate_marker(
                generate_error_marker_path(datapoint.get_intensity()[0].error)
            )

            marker_unshifted = generate_marker(
                generate_error_marker_path(datapoint.get_intensity()[1].error)
            )

            # Scale markersize based on distance
            size_shifted = datapoint.get_intensity()[0].error
            axes.plot(
                datapoint.get_distance().value,
                datapoint.get_intensity()[0].value,
                marker=marker_shifted,
                linestyle="None",
                markersize=size_shifted,
                label=f"Point {index + 1}",
                color=self.main_marker_color,
            )

            size_unshifted = datapoint.get_intensity()[1].error
            axes.plot(
                datapoint.get_distance().value,
                datapoint.get_intensity()[1].value,
                marker=marker_unshifted,
                linestyle="None",
                markersize=size_unshifted,
                label=f"Point {index + 1}",
                color=self.secondary_marker_color,
            )
            index = index + 1

    def plot_fitting_curve(self, datapoints: DatapointCollection, axes: Axes) -> None:
        """
         plotting fitting curve of datapoints
        :param x_data: x coordinates
        :param y_data: y coordinates
        :param axes: the axes on which to draw the fitting curve
        :return: nothing
        """

        # Extracting distance values / intensities of checked datapoints
        checked_datapoints: DatapointCollection = datapoints.get_active_datapoints()

        checked_distances: list[float] = [
            valueErrorPair.value
            for valueErrorPair in checked_datapoints.get_distances()
        ]

        checked_shifted_intensities: list[float] = [
            valueErrorPair.value
            for valueErrorPair in checked_datapoints.get_shifted_intensities()
        ]

        # Calculating coefficients
        coeffs = np.polyfit(
            checked_distances,
            checked_shifted_intensities,
            int(self.parent.menu_bar.number_of_polynomials.get()),
        )

        poly = np.poly1d(coeffs)  # Creating polynomial with given coefficients

        x_fit = np.linspace(min(checked_distances), max(checked_distances), 100)
        y_fit = poly(x_fit)

        # plot the curve
        axes.plot(x_fit, y_fit, color="red", linestyle="--", linewidth="0.6")

    def plot_derivative_curve(
        self, datapoints: DatapointCollection, axes: Axes
    ) -> None:
        """
         plotting derivative curve of datapoints
        :param x_data: x coordinates
        :param y_data: y coordinates
        :param axes: the axes on which to draw the fitting curve
        :return: nothing
        """

        # Extracting distance values / intensities of checked datapoints
        checked_datapoints: DatapointCollection = datapoints.get_active_datapoints()

        checked_distances = checked_datapoints.get_distances().get_values()

        checked_unshifted_intensities = (
            checked_datapoints.get_unshifted_intensities().get_values()
        )

        # Calculating coefficients
        coeffs = np.polyfit(
            checked_distances,
            checked_unshifted_intensities,
            int(self.parent.menu_bar.number_of_polynomials.get()),
        )

        poly = np.poly1d(coeffs)  # Creating polynomial with given coefficients

        x_fit = np.linspace(min(checked_distances), max(checked_distances), 100)
        y_fit = poly(x_fit)

        # plot the curve
        axes.plot(x_fit, y_fit, color="blue", linestyle="-", linewidth="0.6")
