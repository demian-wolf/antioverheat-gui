import tkinter as tk


class BackgroundMixin:
    def set_background(self, background):
        self.__config_recursive(
            self,
            background=background,
            activebackground=background,
        )

    def __config_recursive(self, widget: tk.Misc, **kwargs):
        for key, value in kwargs.items():
            try:
                widget[key] = value
            except tk.TclError:
                pass

        for child in widget.winfo_children():
            self.__config_recursive(child, **kwargs)
