from tkinter import Canvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter
from typing import TYPE_CHECKING

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
            row=0, column=0, rowspan=2, padx=(10, 10), pady=(10, 0), sticky="nsew")
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
        # the figure that will contain the plot
        fig = Figure(figsize=(3, 2), dpi=100, facecolor="white", edgecolor="black")

        # setting color in dependence of appearance mode
        if appearance == "Light":
            main_color = "white"
            secondary_color = "#000000"
        else:
            main_color = "#151515"
            secondary_color = "#ffffff"

        fig.patch.set_facecolor(main_color)

        # list of squares
        y = [(i - 50) ** value for i in range(101)]

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

        # plotting the graph
        plot1.plot(y)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.parent)
        canvas.draw()

        return canvas.get_tk_widget()
