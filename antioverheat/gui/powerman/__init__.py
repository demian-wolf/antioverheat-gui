import tkinter as tk

from .auto_adjust import AutoAdjustControls
from .drag_button import DragButton
from .scale import FrequencyScale


class PowerManager(tk.Tk):
    """The main class of this part of this app."""

    def __init__(self, auto_adjust: bool=False):
        super(PowerManager, self).__init__()

        self.update_idletasks()
        self.overrideredirect(True)

        self.attributes("-topmost", True)

        FrequencyScale(self).grid(row=0, columnspan=2)
        AutoAdjustControls(
            self,
            auto_adjust=auto_adjust,
        ).grid(row=1, columnspan=2)

        tk.Button(
            self,
            text="Close",
            command=self.destroy,
        ).grid(row=3, column=0)

        DragButton(self).grid(row=3, column=1)
