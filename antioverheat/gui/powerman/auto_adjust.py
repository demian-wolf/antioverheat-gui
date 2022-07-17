import tkinter as tk
from tkinter.font import Font
from operator import attrgetter

from antioverheat.backend.api import CPUPowerAPI


class AutoAdjustControls(tk.Frame):
    def __init__(self, *args, **kwargs):
        state = kwargs.pop("auto_adjust", False)

        super(AutoAdjustControls, self).__init__(*args, **kwargs)

        self.state = tk.BooleanVar(self, value=state)

        tk.Checkbutton(
            self,
            text="Auto Adjust",
            font=Font(size=8),
            variable=self.state,
        ).pack(fill=tk.X)

        self.api = CPUPowerAPI()
        self.after(5000, self.step)

    def step(self):
        if self.state.get():
            hottest_core = max(
                self.api.get_cpu_cores(),
                key=attrgetter("value"),
            )
            temperature = hottest_core.value

            self.api.set_policy(max=self._policy_for(temperature))

        self.after(5000, self.step)

    def _policy_for(self, temperature):
        if temperature > 90:
            return self.api.hardware_limits[0]

        current = self.api.get_policy()[-1]

        if temperature > 70:
            return current - 100

        return current + 100
