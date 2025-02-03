import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import tkinter as tk

class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas, window, parent):
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
                self._buttons[tool_name].config(bg='green', relief='flat', highlightthickness=0)

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Path of CustomToolbar.py
        image_path = os.path.join(script_dir, "images", "move_alpha.png")
        image_path_select = os.path.join(script_dir, "images", "move_selected_alpha.png")

        # Ensure Tkinter uses a PhotoImage object
        image = tk.PhotoImage(file=image_path)
        image_select = tk.PhotoImage(file=image_path_select)

        # Change first button image safely
        button_name = self.toolitems[4][0]
        if button_name in self._buttons:
            self._buttons[button_name].config(image=image, selectimage=image_select)
            self._buttons[button_name].image = image
            self._buttons[button_name].selectimage = image_select

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Path of CustomToolbar.py
        zoom_image_path = os.path.join(script_dir, "images", "zoom_blur.png")
        zoom_image_path_select = os.path.join(script_dir, "images", "zoom_selected_blur.png")

        # Ensure Tkinter uses a PhotoImage object
        zoom_image = tk.PhotoImage(file=zoom_image_path)
        zoom_image_select = tk.PhotoImage(file=zoom_image_path_select)

        button_name = self.toolitems[5][0]
        if button_name in self._buttons:
            self._buttons[button_name].config(image=zoom_image, selectimage=zoom_image_select)
            self._buttons[button_name].image = zoom_image
            self._buttons[button_name].selectimage = zoom_image_select



        self.winfo_children()[9].destroy()

        self.winfo_children()[6].destroy()