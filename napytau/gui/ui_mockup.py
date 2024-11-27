import tkinter as tk
from tkinter import Canvas

import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from napytau.cli.cli_arguments import CLIArguments
from napytau.core.logic_mockup import logic

from tkinter import Menu

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


def plot(value, window) -> Canvas:
    # the figure that will contain the plot
    fig = Figure(
                figsize=(3, 2),
                dpi=100,
                facecolor="white",
                edgecolor="black"
                 )
    
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
    def __init__(self):
        super().__init__()
        
        # values
        self.tau = tk.IntVar()
        self.tau.set(2)
        
        # configure window
        self.title("NaPyTau")
        self.geometry(f"{1100}x{580}")
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure((1,2), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create menu bar
        menubar = Menu(self)
        self.config(menu=menubar)

        # =======================================
        #  Create Button "File" in menu bar
        # =======================================
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Read Setup", command=self.read_setup)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # =======================================
        #  Create button "View" in menu bar
        # =======================================
        view_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)

        self.appearance_mode = tk.StringVar(value="system")  # Default: system
        view_menu.add_radiobutton(label="Light mode", variable=self.appearance_mode, value="light",
                                  command=self.change_appearance_mode)
        view_menu.add_radiobutton(label="Dark mode", variable=self.appearance_mode, value="dark",
                                  command=self.change_appearance_mode)
        view_menu.add_radiobutton(label="System", variable=self.appearance_mode, value="system",
                                  command=self.change_appearance_mode)

        # =======================================
        #  Create button "Polynomials" in menu bar
        # =======================================
        poly_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Polynomials", menu=poly_menu)
        number_of_polys_menu = Menu(poly_menu, tearoff=0)
        poly_menu.add_cascade(label="Number of Polynomials", menu=number_of_polys_menu)

        self.number_of_polynomials = tk.StringVar(value="3")  # Default: 3 Polynomials
        for i in range(1, 11):
            number_of_polys_menu.add_radiobutton(label=str(i), variable=self.number_of_polynomials, value=str(i),
                                                 command=self.select_number_of_polynomials)
        poly_menu.add_separator()
        self.polynomial_mode = tk.StringVar(value="Exponential")  # Default: Exponential
        poly_menu.add_radiobutton(label="Equidistant", variable=self.polynomial_mode, value="Equidistant",
                                  command=self.select_polynomial_mode)
        poly_menu.add_radiobutton(label="Exponential", variable=self.polynomial_mode, value="Exponential",
                                  command=self.select_polynomial_mode)

        # =======================================
        #  Create button "Alpha calculation" in menu bar
        # =======================================
        alpha_calc_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Alpha calculation", menu=alpha_calc_menu)

        self.alpha_calc_mode = tk.StringVar(value="sum ratio")
        alpha_calc_menu.add_radiobutton(label="Sum Ratio", variable=self.alpha_calc_mode, value="sum ratio",
                                        command=self.select_alpha_calc_mode)
        alpha_calc_menu.add_radiobutton(label="Weighted Mean", variable=self.alpha_calc_mode, value="weighted mean",
                                        command=self.select_alpha_calc_mode)


        # create sidebar frame with widgets

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="NaPyTau",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, textvariable=self.tau)
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text="calc",
                                                     text_color=("gray10", "#DCE4EE"), command=self.calc)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # create line graph
        self.line_graph = plot(self.tau.get(), self)
        self.line_graph.grid(row=2, column=3, columnspan=1, rowspan=1, padx=(0, 20), pady=(20, 0), sticky="nsew")
        
        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=2, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.slider_2 = customtkinter.CTkSlider(
            self.slider_progressbar_frame,
            variable=self.tau,
            from_=2,
            to=5,
            number_of_steps=3,
            orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        
        # create textbox
        self.label = customtkinter.CTkLabel(self, width=200)
        self.label.grid(row=2, column=1, columnspan=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.slider_2.configure(command=self.use_slider_value)
        self.label.configure(text= "Result: ")


    def open_file(self):
        """
        Opens the file explorer.
        """
        print("open_file")

    def save_file(self):
        """
        Saves the file.
        """
        print("save_file")

    def read_setup(self):
        """
        Reads the setup.
        """
        print("read_setup")

    def quit(self):
        """
        Quits the program.
        """
        print("quit")
        self.destroy()

    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_appearance_mode(self):
        """
        Changes the appearance mode to the variable appearance_mode.
        """
        customtkinter.set_appearance_mode(self.appearance_mode.get())
        print("change appearance mode to " + self.appearance_mode.get())

    def select_number_of_polynomials(self):
        """
        Selects the number of polynomials to use.
        """
        print("selected number of polynomials: " + self.number_of_polynomials.get())

    def select_polynomial_mode(self):
        """
        Selects the polynomial mode.
        """
        print("select polynomial mode " + self.polynomial_mode.get())

    def select_alpha_calc_mode(self):
        """
        Selects the alpha calculation mode.
        """
        print("select alpha calc mode " + self.alpha_calc_mode.get())
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def sidebar_button_event(self):
        print("sidebar_button click")
    
    def use_slider_value(self, _value):
        self.calc()
        
        
        
    def calc(self):
        entry_value = self.tau.get()
        
        self.label.configure(text=f"Result: {logic(entry_value)}")
        self.line_graph = plot(int(entry_value), self)
        self.line_graph.grid(row=2, column=3, columnspan=1, rowspan=1, padx=(0, 20), pady=(20, 0), sticky="nsew")


def init(cli_arguments: CLIArguments):
    app = App()
    app.mainloop()
