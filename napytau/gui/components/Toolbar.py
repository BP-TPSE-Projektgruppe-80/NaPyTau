from tkinter import Canvas
import tkinter as tk
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


class Toolbar():
    def __init__(self, parent,):
        self.parent = parent


        toolbar_frame = tk.Frame(parent)
        toolbar_frame.config(bg="white")
        toolbar_frame.grid(row=0, column=0, sticky="new")  # Use grid for the frame
        toolbar = NavigationToolbar2Tk(self.parent.graph.canvas, toolbar_frame)
        #toolbar.config(bg="white")# Pack inside the frame
        toolbar.update()