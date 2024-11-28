import tkinter as tk
from tkinter import Canvas
from tkinter import Widget

import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from napytau.cli.cli_arguments import CLIArguments
from napytau.core.logic_mockup import logic

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


def plot(value: int, window: Widget) -> Canvas:
    # the figure that will contain the plot
    fig = Figure(figsize=(3, 2), dpi=100, facecolor="white", edgecolor="black")

    # list of squares
    y = [(i - 50) ** value for i in range(101)]

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(y)

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    return canvas.get_tk_widget()


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        # values

        self.tau = tk.IntVar()
        self.tau.set(2)

        # configure window
        self.title("NaPyTau")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure((1, 2), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="NaPyTau",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event
        )
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, textvariable=self.tau)
        self.entry.grid(
            row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )

        self.main_button_1 = customtkinter.CTkButton(
            master=self,
            fg_color="transparent",
            border_width=2,
            text="calc",
            text_color=("gray10", "#DCE4EE"),
            command=self.calc,
        )
        self.main_button_1.grid(
            row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        # create line graph

        self.line_graph = plot(self.tau.get(), self)
        self.line_graph.grid(
            row=2,
            column=3,
            columnspan=1,
            rowspan=1,
            padx=(0, 20),
            pady=(20, 0),
            sticky="nsew",
        )

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(
            self, fg_color="transparent"
        )
        self.slider_progressbar_frame.grid(
            row=2, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.slider_2 = customtkinter.CTkSlider(
            self.slider_progressbar_frame,
            variable=self.tau,
            from_=2,
            to=5,
            number_of_steps=3,
            orientation="vertical",
        )
        self.slider_2.grid(
            row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns"
        )

        # create textbox
        self.label = customtkinter.CTkLabel(self, width=200)
        self.label.grid(
            row=2, column=1, columnspan=1, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.slider_2.configure(command=self.use_slider_value)
        self.label.configure(text="Result: ")

    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str) -> None:
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self) -> None:
        print("sidebar_button click")

    def use_slider_value(self, _value: int) -> None:
        self.calc()

    def calc(self) -> None:
        entry_value = self.tau.get()

        self.label.configure(text=f"Result: {logic(entry_value)}")
        self.line_graph = plot(int(entry_value), self)
        self.line_graph.grid(
            row=2,
            column=3,
            columnspan=1,
            rowspan=1,
            padx=(0, 20),
            pady=(20, 0),
            sticky="nsew",
        )


def init(cli_arguments: CLIArguments) -> None:
    app = App()
    app.mainloop()
