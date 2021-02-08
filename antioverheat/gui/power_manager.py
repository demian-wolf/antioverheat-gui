#!/usr/bin/env python3

# Anti-Overheat Power-Manager
# A Tkinter-based GUI for CPU power management

# (C) Demian Volkov, 2020-2021

import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.font import Font
import tkinter.ttk as ttk
import functools
import subprocess
import operator
import argparse
import os

import colour

from antioverheat.gui.dialogs import GetSudoPasswordDialog
from antioverheat.gui.widgets import DragWinButton
from ..backend.api import CPUPowerAPI
from ..backend.automode import AutomodeThread


class PowerManager(tk.Toplevel):
    """The main class of this part of this app."""
    
    def __init__(self, master, sudo_password, automode):
        super().__init__(master)

        self.api = CPUPowerAPI(sudo_password)

        self.automode_thread = AutomodeThread(sudo_password, enabled=False)
        self.automode_cbtn_var = tk.BooleanVar(self)
        self.automode_cbtn_var.trace("w", self._change_automode_state)
        self.automode_cbtn_var.set(automode)

        self.min_fr, self.max_fr = self.api.hardware_limits
        
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        
        self.scale = tk.Scale(self, orient="vertical",
                              from_=self.min_fr, to=self.max_fr, label="MHz",
                              command=self.change)
        self.scale.grid(row=0, column=0, columnspan=2)

        self.automode_cbtn = tk.Checkbutton(self, text="Automode", font=Font(size=8),
                                            variable=self.automode_cbtn_var)
        self.automode_cbtn.grid(row=1, column=0, columnspan=2, sticky="we")
        
        self.close_btn = tk.Button(self, text="Close", command=self.destroy)
        self.close_btn.grid(row=2, column=0)
        
        self.drag_btn = DragWinButton(self)
        self.drag_btn.grid(row=2, column=1)
        
        self.update_scale()
    
    def change(self, event):
        """This method is called when the scale is moved.
        It applies the changes and calls the update_color() method.

        :param event: tkinter event
        :type event: tkinter.Event
        """
        
        self.api.set_max_fpolicy(self.scale.get())
        self.update_color()

    def _change_automode_state(self, *args, **kwargs):
        self.automode_thread.enabled = self.automode_cbtn_var.get()
        print(self.automode_thread.enabled)
        
    def update_scale(self):
        """This method updates scale every 10 seconds in case the frequency has been changed without using this program."""
        current_frequency = self.api.get_current_fpolicy()[1]
        self.scale.set(current_frequency)
        self.update_color()
        self.after(10000, self.update_scale)

    def update_color(self):
        """This method updates color."""
        value = self.scale.get() - self.min_fr
        color = colour.hsl2hex((abs(value * (1/3) / (self.max_fr - self.min_fr) - (1/3)), 1, 0.5))

        self.configure(background=color)
        for widget in (self.scale, self.automode_cbtn, self.close_btn, self.drag_btn):
            widget.configure(background=color, activebackground=color)