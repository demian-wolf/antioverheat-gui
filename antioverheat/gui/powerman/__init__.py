import tkinter as tk
from tkinter.font import Font

from antioverheat.gui.powerman.scale import FrequencyScale
from antioverheat.gui.widgets import DragWinButton
from antioverheat.backend.api import CPUPowerAPI


class PowerManager(tk.Tk):
    """The main class of this part of this app."""

    def __init__(self, auto):
        super(PowerManager, self).__init__()

        self.api = CPUPowerAPI()

        self.overrideredirect(True)
        self.attributes("-topmost", True)

        self.create_widgets()
        self.automode_var.set(auto)

    def create_widgets(self):
        """Creates the widgets in the window."""

        self.scale = FrequencyScale(self)
        self.scale.grid(row=0, column=0, columnspan=2)

        self.automode_var = tk.BooleanVar()
        self.automode_cbtn = tk.Checkbutton(self, text="Automode", font=Font(size=8),
                                            variable=self.automode_var)
        self.automode_cbtn.grid(row=1, column=0, columnspan=2, sticky="we")
        self.after(5000, self.automode_step)

        self.close_btn = tk.Button(self, text="Close", command=self.destroy)
        self.close_btn.grid(row=2, column=0)

        self.drag_btn = DragWinButton(self)
        self.drag_btn.grid(row=2, column=1)

    def automode_step(self):
        """
        This method stands for one step of "Automode".
        It is called every 5 seconds, and adjusts the CPU frequency depending on its temperature.
        """

        if self.automode_var.get():
            temperature = max(self.api.get_cpu_cores(), key=lambda core: core.value).value
            current_max_policy = self.api.get_policy()[-1]
            if temperature > 90:
                self.api.set_policy(max=self.api.hardware_limits[0])
            elif temperature > 70:
                self.api.set_policy(max=current_max_policy - 100)
            else:
                self.api.set_policy(max=current_max_policy + 100)
            self.scale.refresh()

        self.after(5000, self.automode_step)
