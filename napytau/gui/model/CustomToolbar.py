
from tkinter import Frame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from napytau.gui.app import App

from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk, FigureCanvasTkAgg

class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas: FigureCanvasTkAgg,
                 window: Frame,
                 parent: "App"
                 )-> None:

        super().__init__(canvas, window)

        # Debugging: Print available widgets
        print("Children of toolbar:", self.winfo_children())

        # Change background color of the message label
        self._message_label.config(
            bg=parent.graph.main_color,
            fg=parent.graph.secondary_color,
            font=('Arial', 10)
        )

        # Customize specific buttons
        for toolitem in self.toolitems:
            tool_name = toolitem[0]  # Get button name
            if tool_name in self._buttons:
                self._buttons[tool_name].config(bg='green',
                                                relief='flat',
                                                highlightthickness=0
                                                )



        self.winfo_children()[9].destroy()

        self.winfo_children()[6].destroy()