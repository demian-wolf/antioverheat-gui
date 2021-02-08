import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tk_msgbox
import functools
import argparse
import sys
import os

from antioverheat.gui.dialogs import GetSudoPasswordDialog
from antioverheat.backend.misc import verify_sudo_pwd
from antioverheat.gui import PowerManager, OverheatNotification


def main():
    root = tk.Tk()
    root.withdraw()

    uid = os.getuid()
    if uid == 0:
        tk_msgbox.showerror("Error", "Please DO NOT run this program as root!")
        sys.exit(1)

    args_parser = argparse.ArgumentParser()

    args_parser.add_argument("-powerman",
                             action="store_true",
                             help="launch power manager")
    args_parser.add_argument("-p",
                             "--password",
                             help="your user password (necessary to execute commands through sudo)")
    args_parser.add_argument("-a",
                             "--automode",
                             action="store_true",
                             help="enable automode (the temperature is adjusted automatically based on the CPU temperature)")

    args_parser.add_argument("-tempmon",
                             action="store_true",
                             help="launch temperature monitor")
    args_parser.add_argument("-s",
                             "--sound",
                             action="store_true",
                             help="enable sound notification by default")
    args_parser.add_argument("-i",
                             "--interval",
                             type=int,
                             help="refresh frequency (in ms). Default value is 500 ms.")

    args = args_parser.parse_args()

    if not args.tempmon and (args.sound or args.interval):
        tk_msgbox.showwarning("Invalid args", "Some tempmon args were specified without -tempmon arg. "
                                              "Tempmon will not be launched, and these args will be ignored")
    if not args.powerman and (args.password or args.automode):
        tk_msgbox.showwarning("Invalid args", "Automode was enabled or password was specified without -powerman arg. "
                                              "Powerman will not be launched, and the args will be ignored.")

    if args.powerman:
        if args.password:
            sudo_password = args.password
            if not verify_sudo_pwd(sudo_password):
                tk_msgbox.showerror("Error", "You have provided a wrong password!")
                sys.exit(1)
        else:
            sudo_password = GetSudoPasswordDialog(root).data
            if sudo_password is None:
                tk_msgbox.showerror("Error",
                                    "No sudo password has been provided. This program will now exit.")
                sys.exit(1)
        root.after(0, PowerManager, root, sudo_password, args.automode)

    if args.tempmon:
        if args.interval is None:
            args.interval = 500
        root.after(0, OverheatNotification, root, args.sound, args.interval)

    root.mainloop()

main()