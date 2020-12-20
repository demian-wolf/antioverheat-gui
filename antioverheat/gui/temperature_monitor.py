#!/usr/bin/env python3

# Anti-Overheat Temperature-Monitor
# A Tkinter-based GUI that notifies about CPU overheat

# (C) Demian Wolf 2020


from functools import partial
import tkinter as tk
import tkinter.ttk as ttk
import threading
import argparse
import subprocess
import os
import time

import colour

import core


# TODO: add logging

class Notification(tk.Tk):
    """The main class of this part of this app."""
    def __init__(self, sound_notification=False, refresh_interval=500):
        super().__init__()

        self.sound_notification = bool(sound_notification)
        self.refresh_interval = refresh_interval        

        self.overrideredirect(True)
        self.attributes("-topmost", True)

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

        self.after(0, self.refresh)

    def init_treeview(self):
        """Inits `self.cores_tree`.
        Called only once
        """
        cpu_cores = list(core.get_cpu_cores())

        columns = ["#{}".format(no) for no in range(1, len(cpu_cores) + 1)]
        self.cores_tree.configure(columns=columns)
        
        for column, cpu_core in zip(columns, cpu_cores):
            self.cores_tree.heading(column, text=cpu_core[0])
            self.cores_tree.column(column, anchor="center")
        
    def refresh(self):
        """Refreshes the notfication window.

        If there is no overheat -- it is withdrawn.
        Otherwise it is deiconified; the color of the notification
        and the values in the `self.cores_tree` are updated.
        
        Also the sound notification is played, if enabled.

        It is called every 500 ms by default.
        """

        def __raw2celsius(raw):
            if isinstance(raw, float):
                if raw.is_integer():
                   raw = int(raw)
            if isinstance(raw, (float, int)):
                return "{} \u00b0C".format(raw)
            raise TypeError("raw must be either int or float, not {}".format(type(raw)))
        
        cpu_cores = list(core.get_cpu_cores())
        
        for cpu_core in cpu_cores:
            if cpu_core[1] >= 75:
                self.deiconify()
                self.geometry("+{}+{}"\
                              .format(self.winfo_screenwidth() // 2 - self.winfo_width() // 2, 0))
                if self.sound_notification:
                    subprocess.Popen("play -nq -t alsa synth 0.35 sine 1000", shell=True)
                break
        else:
            self.withdraw()
            
        if self.winfo_viewable():
            temp_values = [cpu_core[1] for cpu_core in cpu_cores]
            color = colour.hsl2hex(((120 - max(temp_values)) / 360, 1, 0.5))
            for widget in (self.title_frame, *self.title_frame.winfo_children()):
                widget.configure(bg=color)
            prettified_tvs = [__raw2celsius(temp_value) for temp_value in temp_values]
            self.cores_tree.delete(*self.cores_tree.get_children())
            self.cores_tree.insert("", "end", values=prettified_tvs)
            
        self.after(self.refresh_interval, self.refresh)

def main():
    root = tk.Tk()
    root.withdraw()
    
    uid = os.getuid()
    if uid == 0:
        showerror("Error", "Please DO NOT run this program as root!")
        return

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-s",
                             "--sound",
                             action="store_true",
                             help="enable sound notification by default")
    args_parser.add_argument("-i",
                             "--interval",
                             default=500,
                             type=int,
                             help="refresh frequency (in ms). Default value is 500 ms.")
    args = args_parser.parse_args()

    root.destroy()
    
    Notification(sound_notification=args.sound, refresh_interval=args.interval).mainloop()
    
if __name__ == "__main__":
    main()
