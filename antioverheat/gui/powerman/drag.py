import tkinter as tk


class DragButton(tk.Button):
    """
    The button for dragging the parent window.
    """
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("text", "\u2630")

        super().__init__(*args, **kwargs)

        self.root = self.winfo_toplevel()

        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.on_move)

    def start_move(self, event):
        """
        This method is called when the user presses the button.

        :param event: tkinter event
        :type event: tkinter.Event
        """
        
        self.config(cursor="fleur")

        self.x = event.x
        self.y = event.y

    def stop_move(self, _event):
        """
        This method is called when the user releases the button.

        :param event: tkinter event
        :type event: tkinter.Event
        """
        
        self.config(cursor="")

        self.x = None
        self.y = None

    def on_move(self, event):
        """
        This method calculates and sets coordinates of the window.

        :param event: tkinter event
        :type event: tkinter.Event
        """

        x = self.root.winfo_x() + event.x - self.x
        y = self.root.winfo_y() + event.y - self.y

        bottom = self.winfo_screenheight() - self.root.winfo_height()
        right = self.winfo_screenwidth() - self.root.winfo_width()

        if y < 0:
            y = 0
        elif y > bottom:
            y = bottom

        if x < 0:
            x = 0
        elif x > right:
            x = right

        self.root.geometry(f"+{x}+{y}")
