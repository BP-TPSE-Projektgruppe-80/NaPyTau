import customtkinter
from typing import TYPE_CHECKING

from napytau.gui.model.log_message_type import LogMessageType

if TYPE_CHECKING:
    from napytau.gui.app import App  # Import only for the type checking.

class ControlPanel(customtkinter.CTkFrame):
    def __init__(self, parent: "App"):
        """
        The panel with all the controls, inputs etc.
        :param parent: Parent widget to host the control panel.
        """
        super().__init__(parent, corner_radius=10)
        self.parent = parent

        # Main area for buttons and controls
        self.grid(row=1, column=1, rowspan=2, padx=(0, 10), pady=(10, 10),
                  sticky="nsew")
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_propagate(True)

        self.timescale = customtkinter.DoubleVar(value=1.0)
        self.result_chi2 = customtkinter.StringVar(value="N/A")
        self.result_tau = customtkinter.StringVar(value="N/A")
        self.result_tau_error = customtkinter.StringVar(value="N/A")
        self.result_abs_tau_t = customtkinter.StringVar(value="N/A")

        self._create_widgets()

    def _create_widgets(self) -> None:
        """
        Create the control panel widgets.
        """
        # Row 1: Timescale Controls
        timescale_widget = self._create_timescale_widget()
        timescale_widget.pack(fill="x", padx=5, pady=5)

        # Row 2: Chi^2 Display
        chi2_widget = self._create_chi2_widget()
        chi2_widget.pack(fill="x", padx=5, pady=5)

        # Row 3: Tau Display
        tau_widget = self._create_tau_widget()
        tau_widget.pack(fill="x", padx=5, pady=5)

        # Row 4: Abs(Tau - T) Display
        abs_tau_t_widget = self._create_abs_tau_t_widget()
        abs_tau_t_widget.pack(fill="x", padx=5, pady=5)

    def _create_timescale_widget(self) -> customtkinter.CTkFrame:
        """
        Create the timescale widget.
        """
        min_timescale = 0.01
        max_timescale = 100.0

        frame = customtkinter.CTkFrame(self)

        timescale_entry = customtkinter.StringVar(value=str(self.timescale.get()))

        def update_timescale() -> None:
            try:
                value = float(timescale_entry.get())
                if min_timescale <= value <= max_timescale:
                    self.timescale.set(value)
                    self.parent.logger.log_message(
                        f"Timescale set to: {value}", LogMessageType.INFO)
                else:
                    self.parent.logger.log_message(
                        f"Error: Value out of valid range ({min_timescale:.2f}"
                        f" - {max_timescale:.2f}).",
                        LogMessageType.ERROR)
            except ValueError:
                self.parent.logger.log_message(
                    "Invalid input value, please enter a number.",
                    LogMessageType.ERROR)

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

    def _create_chi2_widget(self) -> customtkinter.CTkFrame:
        """
        Create the chi^2 widget.
        """
        frame = customtkinter.CTkFrame(self)
        button = customtkinter.CTkButton(frame, text="Minimize",
                                         command=self._chi2_button_event)
        button.pack(side="left", padx=5)

        label = customtkinter.CTkLabel(frame, text="χ²:")
        label.pack(side="left", padx=15)

        result = customtkinter.CTkLabel(frame, textvariable=self.result_chi2)
        result.pack(side="left", padx=5)

        return frame

    def _create_tau_widget(self) -> customtkinter.CTkFrame:
        """
        Create the tau widget.
        """
        frame = customtkinter.CTkFrame(self)

        button = customtkinter.CTkButton(frame, text="τ ± Δτ [ps]:",
                                         command=self._tau_button_event)
        button.pack(side="left", padx=5)

        result = customtkinter.CTkLabel(frame, textvariable=self.result_tau)
        result.pack(side="left", padx=5)

        separator = customtkinter.CTkLabel(frame, text="±")
        separator.pack(side="left", padx=5)

        error = customtkinter.CTkLabel(frame, textvariable=self.result_tau_error)
        error.pack(side="left", padx=5)

        return frame

    def _create_abs_tau_t_widget(self) -> customtkinter.CTkFrame:
        """
        Create the abs tau t widget.
        """
        frame = customtkinter.CTkFrame(self)

        button = customtkinter.CTkButton(frame, text="Absolute τ",
                                         command=self._absolute_tau_button_event)
        button.pack(side="left", padx=5)

        label = customtkinter.CTkLabel(frame, text="|τ - t| [ps]:")
        label.pack(side="left", padx=15)

        result = customtkinter.CTkLabel(frame, textvariable=self.result_abs_tau_t)
        result.pack(side="left", padx=5)

        return frame

    def _timescale_button_event(self) -> None:
        """
        Event if the timescale button is clicked.
        """
        print(f"Timescale set to {self.timescale.get():.2f} ps")

    def _timescale_slider_event(self, value: str) -> None:
       """
       Event for the timescale slider.
       :param value: The current value of the slider.
       """
       self.timescale.set(round(float(value), 2))

    def _tau_button_event(self) -> None:
        """
        Event if the tau button is clicked.
        """
        self.set_result_tau(0.0)
        self.set_result_tau_error(0.0)

    def _chi2_button_event(self) -> None:
        """
        Event if the chi2 button is clicked.
        """
        self.set_result_chi2(0.0)

    def _absolute_tau_button_event(self) -> None:
        """
        Event if the absolute tau button is clicked.
        """
        self.set_result_abs_tau_t(0.0)

    def set_result_chi2(self, chi2: float) -> None:
        """
        Set the chi^2 value.
        :param chi2: The new value for chi2.
        """
        self.result_chi2.set(chi2)

    def set_result_tau(self, tau: float) -> None:
        """
        Set the tau value.
        :param tau: The new value for tau.
        """
        self.result_tau.set(tau)

    def set_result_tau_error(self, tau_error: float) -> None:
        """
        Set the tau error value.
        :param tau_error: The new value for the tau error.
        """
        self.result_tau_error.set(tau_error)

    def set_result_abs_tau_t(self, abs_tau_t: float) -> None:
        """
        Set the absolute tau value.
        :param abs_tau_t:  The new value for the absolute tau value.
        """
        self.result_abs_tau_t.set(abs_tau_t)