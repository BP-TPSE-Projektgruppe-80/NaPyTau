import tkinter as tk


from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.


class Toolbar():
    def __init__(self, parent: "App") -> None:
        self.parent = parent

        #Create frame to hold Toolbar

        toolbar_frame = tk.Frame(parent)
        toolbar_frame.config(bg="white")
        toolbar_frame.grid(row=0,
                           column=0,
                           padx=10,
                           pady=10,
                           sticky="new"
                           )

        #Create Toolbar

        toolbar = NavigationToolbar2Tk(self.parent.graph.canvas,
                                       toolbar_frame)
        #Adjust background color
        toolbar.config(bg=self.parent.graph.main_color)
        toolbar.update()

