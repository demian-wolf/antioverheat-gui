import tkinter as tk

from antioverheat.gui.powerman.auto_adjust import AutoAdjustControls
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

        self.scale = FrequencyScale(self)
        self.scale.grid(row=0, column=0, columnspan=2)

        self.auto_adjust = AutoAdjustControls(self)
        self.auto_adjust.grid(row=1, column=0, columnspan=2)

        self.close_btn = tk.Button(self, text="Close", command=self.destroy)
        self.close_btn.grid(row=2, column=0)

        self.drag_btn = DragWinButton(self)
        self.drag_btn.grid(row=2, column=1)
