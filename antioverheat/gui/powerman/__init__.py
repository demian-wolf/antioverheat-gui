import tkinter as tk
from tkinter.font import Font

import colour

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

        self.update_scale(recursive=True)

    def create_widgets(self):
        """Creates the widgets in the window."""

        self.scale = tk.Scale(self, orient="vertical", label="MHz", command=self.change)
        self.scale["from_"], self.scale["to"] = self.api.hardware_limits
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

    def change(self, event):
        """This method is called when the scale is being moved.
        It applies the CPU frequency changes and calls the update_color() method.

        :param event: tkinter event
        :type event: tkinter.Event
        """

        self.api.set_policy(max=self.scale.get())
        self.update_color()

    def update_scale(self, recursive=False):
        """This method updates the scale with the precise data
        in case CPU frequency was changed by another app.

        if recursive is enabled, it is automatically called every 10 seconds."""

        current_policy = self.api.get_policy()

        self.scale.set(current_policy[1])
        self.update_color()

        if recursive:
            self.after(10000, self.update_scale, True)

    def update_color(self):
        """This method updates color of the scale every time the policy has been changed."""

        min_frequency, max_frequency = self.api.hardware_limits

        value = self.scale.get() - min_frequency
        color = colour.hsl2hex((abs(value * (1/3) / (max_frequency - min_frequency) - (1/3)), 1, 0.5))

        self.configure(background=color)
        for widget in (self.scale, self.automode_cbtn, self.close_btn, self.drag_btn):
            widget.configure(background=color, activebackground=color)

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
            self.update_scale(recursive=False)

        self.after(5000, self.automode_step)
