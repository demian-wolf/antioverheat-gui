import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tk_msgbox

from ...backend.misc import verify_sudo_pwd


class GetSudoPasswordDialog(tk.Toplevel):
    """Dialog for getting sudo password.

    :param master: master window
    :type master: tkinter.Tk
    """
    
    def __init__(self, master, title=None, prompt=None):
        super().__init__(master)

        title = title or "Sudo Password"
        prompt = prompt or "Please enter your user password (the same you use with sudo):"
        
        self.data = None
        
        self.resizable(False, False)
        self.title(title)
        
        input_frame = tk.Frame(self)
        tk.Label(input_frame, text=prompt).grid(row=0, column=0)
        self.entry = ttk.Entry(input_frame, show="\u25cf")
        self.entry.bind("<Return>", self.ok)
        self.entry.grid(row=0, column=1)
        self.entry.focus_force()
        input_frame.pack()
        
        buttons_frame = tk.Frame(self)
        ttk.Button(buttons_frame, text="OK", command=self.ok)\
                                  .grid(row=0, column=0, padx=2, pady=5)
        ttk.Button(buttons_frame, text="Cancel", command=self.destroy)\
                                  .grid(row=0, column=1, padx=2, pady=5)
        buttons_frame.pack()
        
        self.wait_visibility()
        self.grab_set()
        self.center()
        self.wait_window(self)

    def ok(self, event=None):
        """This method is being called when the OK button of the dialog is clicked.

        :param event: tkinter event (optional)
        :type event: tkinter.Event
        """
        
        data = self.entry.get()
        if not verify_sudo_pwd(data):
            tk_msgbox.showerror("Error", "You entered a wrong password!")
            return
        self.data = data
        self.destroy()
        
    def center(self):
        """Center this dialog window"""
     
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))

        self.geometry("+{}+{}".format(x_cordinate, y_cordinate))
