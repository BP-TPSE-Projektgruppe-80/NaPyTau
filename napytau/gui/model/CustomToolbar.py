import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import tkinter as tk


class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas, window, parent):
        super().__init__(canvas, window)

        # Change background color


        print(self.winfo_children())

        self._message_label.config(bg=parent.graph.main_color, fg= parent.graph.secondary_color , font=('Arial', 10))



        self.winfo_children()[9].destroy()




        # Customize specific buttons
        for toolitem in self.toolitems:
            if toolitem[0] in self._buttons:
                self._buttons[toolitem[0]].config(bg='green', relief='flat', highlightthickness=0)
                print(toolitem[0])