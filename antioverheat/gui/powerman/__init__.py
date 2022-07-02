import tkinter as tk

from antioverheat.gui.powerman.auto_adjust import AutoAdjustControls
from antioverheat.gui.powerman.scale import FrequencyScale
from antioverheat.gui.widgets import DragWinButton


class PowerManager(tk.Tk):
    """The main class of this part of this app."""

    def __init__(self, auto_adjust=False):
        super(PowerManager, self).__init__()

        self.update_idletasks()
        self.overrideredirect(True)

        self.attributes("-topmost", True)

        FrequencyScale(self).grid(row=0, columnspan=2)
        AutoAdjustControls(self).grid(row=1, columnspan=2)

        tk.Button(
            self,
            text="Close",
            command=self.destroy,
        ).grid(row=3, column=0)

        DragWinButton(self).grid(row=3, column=1)
