import argparse
import os
import sys
import tkinter as tk
import tkinter.messagebox as tk_msgbox

from antioverheat.gui import PowerManager, OverheatNotification


def main():
    root = tk.Tk()
    root.withdraw()

    # TODO: require root privileges only for tempmon
    uid = os.getuid()
    if uid != 0:
        tk_msgbox.showerror("Error", "This app requires root privileges!")
        sys.exit(1)

    args_parser = argparse.ArgumentParser()

    args_parser.add_argument("-powerman",
                             action="store_true",
                             help="launch power manager")
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
    if not args.powerman and args.automode:
        tk_msgbox.showwarning("Invalid args", "Automode arg was specified without -powerman arg."
                                              "Powerman will not be launched, and the args will be ignored.")

    if args.powerman:
        root.after(0, PowerManager, root, args.automode)

    if args.tempmon:
        if args.interval is None:
            args.interval = 500
        root.after(0, OverheatNotification, root, args.sound, args.interval)

    root.mainloop()

main()