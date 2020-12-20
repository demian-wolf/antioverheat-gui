#!/usr/bin/env python3

# Anti-Overheat Power-Manager
# A Tkinter-based GUI for CPU power management

# (C) Demian Volkov, 2020

import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.font import Font
import tkinter.ttk as ttk
import functools
import subprocess
import argparse
import os

import colour

from custom_dialogs import GetSudoPasswordDialog
from custom_widgets import DragWinButton
import core
import misc


class PowerManager(tk.Tk):
    """The main class of this part of this app."""
    
    def __init__(self, sudo_password):
        super().__init__()

        self.min_fr, self.max_fr = core.get_hardware_limits()

        self.sudo_password = sudo_password
        
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        
        self.scale = tk.Scale(self, orient="vertical",
                              from_=self.min_fr, to=self.max_fr, label="MHz",
                              command=self.change)
        self.scale.grid(row=0, column=0, columnspan=2)

        self.aa_cbtn = tk.Checkbutton(self, text="Anti-Overheat", font=Font(size=8))
        self.aa_cbtn.grid(row=1, column=0, columnspan=2, sticky="we")
        
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
        
        core.set_max_fpolicy(self.sudo_password, self.scale.get())
        self.update_color()
        
    def update_scale(self):
        """This method updates scale every 10 seconds in case the frequency has been changed without using this program."""
        current_frequency = core.get_current_fpolicy()[1]
        self.scale.set(current_frequency)
        self.update_color()
        self.after(10000, self.update_scale)

    def update_color(self):
        """This method updates color."""
        value = self.scale.get() - self.min_fr
        color = colour.hsl2hex((abs(value * (1/3) / (self.max_fr - self.min_fr) - (1/3)), 1, 0.5))

        self.configure(background=color)
        for widget in (self.scale, self.aa_cbtn, self.close_btn, self.drag_btn):
            widget.configure(background=color, activebackground=color)

# TODO: sys.exit(1) after every error message rather than just return

def main():
    root = tk.Tk()
    root.withdraw()
    
    uid = os.getuid()
    if uid == 0:
        showerror("Error", "Please DO NOT run this program as root!")
        return
    
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-p",
                           "--password",
                           help="your user password (necessary to execute commands through sudo)")
    args = args_parser.parse_args()
    
    if args.password:
        sudo_password = args.password
        if not misc.verify_sudo_pwd(sudo_password):
            showerror("Error", "You have provided a wrong password!")
            return
    else:
        sudo_password = GetSudoPasswordDialog(root).data
        if sudo_password is None:
            showerror("Error",
                      "No sudo password has been provided. This program will now exit.")
            return

    root.destroy()

    PowerManager(sudo_password=sudo_password).mainloop()

if __name__ == "__main__":
    main()
