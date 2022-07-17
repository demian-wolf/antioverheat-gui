import tkinter as tk
import tkinter.ttk as ttk
import subprocess

import colour

from antioverheat.backend.api import CPUPowerAPI


# TODO: add logging

class OverheatNotification(tk.Toplevel):
    """The main class of this part of this app."""
    def __init__(self, master, sound, refresh):
        super().__init__(master)

        self.api = CPUPowerAPI()

        self.sound = sound
        self.interval = refresh

        self.overrideredirect(True)
        self.attributes("-topmost", True)

        self.create_widgets()

        self.after(0, self.refresh)

    def create_widgets(self):
        """Creates the widgets in the window."""

        self.title_frame = tk.Frame(self)
        tk.Label(self.title_frame,
                 image="::tk::icons::warning").pack(side="left", anchor="center")
        tk.Label(self.title_frame, bg="red",
                 text="CPU Overheat Warning!",
                 font="Arial 36 bold").pack(side="left", anchor="e")
        self.title_frame.pack()

        self.cores_tree = ttk.Treeview(self, height=1, show="headings")
        self.init_treeview()
        self.cores_tree.pack(fill="x")

    def init_treeview(self):
        """Prepares `self.cores_tree` for displaying real-time CPU temperature.
        Should be called only once.
        """
        cpu_cores = list(self.api.get_cpu_cores())

        columns = ["#{}".format(no) for no in range(1, len(cpu_cores) + 1)]
        self.cores_tree.configure(columns=columns)

        for column, cpu_core in zip(columns, cpu_cores):
            self.cores_tree.heading(column, text=cpu_core.name)
            self.cores_tree.column(column, anchor="center")

    def refresh(self):
        """Refreshes the notfication window.

        If there is no overheat, it is withdrawn.
        Otherwise, it is deiconified; the color of the notification
        and the values in the `self.cores_tree` are updated.

        Also the sound notification is played, if enabled.

        By default, it is called every 500 ms (self.refresh_interval).
        """

        def __raw2celsius(raw):
            if isinstance(raw, float):
                if raw.is_integer():
                    raw = int(raw)
            if isinstance(raw, int):
                return "{} \u00b0C".format(raw)
            raise TypeError("raw must be either int or float, not {}".format(type(raw)))

        cpu_cores = list(self.api.get_cpu_cores())

        for cpu_core in cpu_cores:
            if cpu_core.value >= 75:
                self.deiconify()
                self.geometry("+{}+{}" \
                              .format(self.winfo_screenwidth() // 2 - self.winfo_width() // 2, 0))
                if self.sound:
                    subprocess.Popen("play -nq -t alsa synth 0.35 sine 1000", shell=True)
                break
        else:
            self.withdraw()

        if self.winfo_viewable():
            temp_values = [cpu_core.value for cpu_core in cpu_cores]
            color = colour.hsl2hex(((120 - max(temp_values)) / 360, 1, 0.5))
            for widget in (self.title_frame, *self.title_frame.winfo_children()):
                widget.configure(bg=color)
            prettified_tvs = [__raw2celsius(temp_value) for temp_value in temp_values]
            self.cores_tree.delete(*self.cores_tree.get_children())
            self.cores_tree.insert("", "end", values=prettified_tvs)

        self.after(self.refresh, self.refresh)
