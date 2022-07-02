from typing import Any
import functools
import tkinter as tk

from colour import hsl2hex

from antioverheat.backend.api import CPUPowerAPI


class FrequencyScale(tk.Scale):
    def __init__(self, *args, **kwargs):
        self.api = CPUPowerAPI()
        self.max_value, self.min_value = self.api.hardware_limits

        kwargs.setdefault("orient", "vertical")
        kwargs.setdefault("label", "MHz")

        super(FrequencyScale, self).__init__(*args, **kwargs)

        self.configure(
            command=self.command,
            from_=self.max_value,
            to=self.min_value,
        )

        self.after_idle(self.refresh, True)

    def command(self, value: Any) -> None:
        self.event_generate(
            "<<FrequencyUpdate>>",
            data=int(value),
        )

    def refresh(self, recursive: bool = False) -> None:
        value = self.api.get_policy()[1]
        self.set(value)

        if recursive:
            self.after(10_000, self.refresh)

    @functools.lru_cache(maxsize=None)
    def _value2background(self, value: int) -> str:
        ratio = (value - self.min_value) / (self.max_value - self.min_value)

        return hsl2hex([(1 - ratio) / 3, 1, 0.5])
