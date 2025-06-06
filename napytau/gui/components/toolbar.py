import tkinter as tk


from typing import TYPE_CHECKING

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from napytau.gui.model.custom_toolbar import CustomToolbar

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.


class Toolbar:
    def __init__(self, parent: "App", canvas: FigureCanvasTkAgg) -> None:
        self.parent = parent

        # Create frame to hold Toolbar

        toolbar_frame = tk.Frame(parent)
        toolbar_frame.config(bg=self.parent.graph.main_color)
        toolbar_frame.grid(row=1, column=0, padx=10, pady=10, sticky="new")

        # Create Toolbar

        toolbar = CustomToolbar(canvas, toolbar_frame, parent)
        # Adjust background color
        toolbar.config(bg=self.parent.graph.main_color)
        toolbar.update()
