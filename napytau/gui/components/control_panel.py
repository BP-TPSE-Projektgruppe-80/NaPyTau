import customtkinter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.


class ControlPanel(customtkinter.CTkFrame):
    def __init__(self, parent: "App"):
        """
        The panel with all the control needed.
        :param parent: Parent widget to host the control panel.
        """
        super().__init__(parent, corner_radius=10)
        self.parent = parent

        # Main area for buttons and controls
        self.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_propagate(True)

        self.timescale = customtkinter.DoubleVar(value=1.0)
        self.result_chi2 = customtkinter.StringVar(value="N/A")
        self.result_tau = customtkinter.StringVar(value="N/A")
        self.result_tau_error = customtkinter.StringVar(value="N/A")
        self.result_abs_tau_t = customtkinter.StringVar(value="N/A")

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create the control panel widgets.
        """
        # Row 1: Timescale Controls
        timescale_widget = self.create_timescale_widget()
        timescale_widget.pack(fill="x", padx=5, pady=5)

        # Row 2: Chi^2 Display
        chi2_widget = self.create_chi2_widget()
        chi2_widget.pack(fill="x", padx=5, pady=5)

        # Row 3: Tau Display
        tau_widget = self.create_tau_widget()
        tau_widget.pack(fill="x", padx=5, pady=5)

        # Row 4: Abs(Tau - T) Display
        abs_tau_t_widget = self.create_abs_tau_t_widget()
        abs_tau_t_widget.pack(fill="x", padx=5, pady=5)

    def create_timescale_widget(self) -> customtkinter.CTkFrame:
        """
        Create the timescale widget.
        """
        min_timescale = 0.01
        max_timescale = 100.0

        frame = customtkinter.CTkFrame(self)

        timescale_entry = customtkinter.StringVar(value=str(self.timescale.get()))

        # TODO: Print errors to the logger later on.
        def update_timescale() -> None:
            try:
                value = float(timescale_entry.get())
                if min_timescale <= value <= max_timescale:
                    self.timescale.set(value)
                    print(f"Timescale set to: {value}")
                else:
                    print(f"Error: Value out of valid range ({min_timescale:.2f}"
                          f" - {max_timescale:.2f}).")
            except ValueError:
                print("Error: Invalid input value, please enter a number.")

        def sync_entry_with_slider(value : float) -> None:
            timescale_entry.set(f"{value:.2f}")

        button = customtkinter.CTkButton(frame, text="t [ps]",
                                         command=update_timescale)
        button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        entry = customtkinter.CTkEntry(frame, textvariable=timescale_entry,
                                       justify="right", width=80)
        entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        slider = customtkinter.CTkSlider(frame, from_=min_timescale, to=max_timescale,
                                         variable=self.timescale,
                                         command=sync_entry_with_slider)
        slider.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        return frame

    def create_chi2_widget(self) -> customtkinter.CTkFrame:
        """
        Create the chi^2 widget.
        """
        frame = customtkinter.CTkFrame(self)

        label = customtkinter.CTkLabel(frame, text="χ²:")
        label.pack(side="left", padx=15)

        result = customtkinter.CTkLabel(frame, textvariable=self.result_chi2)
        result.pack(side="left", padx=5)

        return frame

    def create_tau_widget(self) -> customtkinter.CTkFrame:
        """
        Create the tau widget.
        """
        frame = customtkinter.CTkFrame(self)

        button = customtkinter.CTkButton(frame, text="τ ± Δτ [ps]:",
                                         command=self.tau_button_event)
        button.pack(side="left", padx=5)

        result = customtkinter.CTkLabel(frame, textvariable=self.result_tau)
        result.pack(side="left", padx=5)

        error = customtkinter.CTkLabel(frame, textvariable=self.result_tau_error)
        error.pack(side="left", padx=5)

        return frame

    def create_abs_tau_t_widget(self) -> customtkinter.CTkFrame:
        """
        Create the abs tau t widget.
        """
        frame = customtkinter.CTkFrame(self)

        label = customtkinter.CTkLabel(frame, text="|τ - t| [ps]:")
        label.pack(side="left", padx=15)

        result = customtkinter.CTkLabel(frame, textvariable=self.result_abs_tau_t)
        result.pack(side="left", padx=5)

        return frame

    def timescale_button_event(self) -> None:
        """
        Event if the timescale button is clicked.
        """
        print(f"Timescale set to {self.timescale.get():.2f} ps")

    def timescale_slider_event(self, value: str) -> None:
       """
       Event for the timescale slider.
       :param value: The current value of the slider.
       """
       self.timescale.set(round(float(value), 2))

    def tau_button_event(self) -> None:
        """
        Event if the tau button is clicked.
        """
        print("Tau button clicked")