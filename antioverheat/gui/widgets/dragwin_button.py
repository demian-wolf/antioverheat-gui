import tkinter as tk


class DragWinButton(tk.Button):
    """This is a class for "Drag" button, which is used for dragging
    the window of the program.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(text="☰", *args, **kwargs)

        self.root_window = self.winfo_toplevel()

        for event, func in (("<ButtonPress-1>", self.start_move),
                            ("<ButtonRelease-1>", self.stop_move),
                            ("<B1-Motion>", self.do_move)):
            self.bind(event, func)

    def start_move(self, event):
        """This method is called when the user presses the "Drag".
        :param event: tkinter event
        :type event: tkinter.Event
        """
        
        self.config(cursor="fleur")
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        """This method is called when the user releases the "Drag" button.
        :param event: tkinter event
        :type event: tkinter.Event
        """
        
        self.config(cursor="")
        self.x = None
        self.y = None

    def do_move(self, event):
        """This method is called while the window is being moved by user.

        This method calculates and sets new coordinates of the window.

        :param event: tkinter event
        :type event: tkinter.Event
        """

        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root_window.winfo_x() + deltax
        y = self.root_window.winfo_y() + deltay

        upper_point = 0
        bottom_point = self.winfo_screenheight() - self.root_window.winfo_height()
        left_point = 0
        right_point = self.winfo_screenwidth() - self.root_window.winfo_width()
        
        if y < upper_point:
            y = upper_point
        elif y > bottom_point:
            y = bottom_point

        if x < left_point:
            x = left_point
        elif x > right_point:
            x = right_point

        self.root_window.geometry("+{}+{}".format(x, y))
        self.master.attributes("-topmost", True)
