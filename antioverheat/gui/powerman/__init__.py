from functools import lru_cache
import tkinter as tk

from colour import hsl2hex

from antioverheat.backend.api import CPUPowerAPI
from antioverheat.gui.common import App, DragButton
from .auto_adjust import AutoAdjustControls


class PowerManager(App):
    """The main class of this part of this app."""

    def __init__(self, auto_adjust: bool=False):
        self.api = CPUPowerAPI()

        super(PowerManager, self).__init__()

        self.overrideredirect(True)
        self.attributes("-topmost", True)

        self.scale = tk.Scale(
            self,
            command=self.on_set,
            orient=tk.VERTICAL,
            label="MHz",
            from_=self.api.hardware_limits[0],
            to=self.api.hardware_limits[1],
        )
        self.scale.grid(row=0, columnspan=2)

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

        self.after_idle(self.refresh, True)

    def on_set(self, value: str) -> None:
        value = int(value)

        self.set_background(
            self.value2background(value, *self.api.hardware_limits),
        )

    def refresh(self, recursive: bool = False) -> None:
        value = self.api.get_policy()[1]
        self.scale.set(value)

        if recursive:
            self.after(10_000, self.refresh, True)

    @staticmethod
    @lru_cache(maxsize=None)
    def value2background(value: int, min_value: int, max_value: int) -> str:
        ratio = (value - min_value) / (max_value - min_value)

        return hsl2hex([(1 - ratio) / 3, 1, 0.5])
