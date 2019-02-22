import tkinter as tk
from guiEXT import login


class App(tk.Tk):
    """"the main application, subclassing Tk"""
    def __init__(self):
        """
        Initisizes the main application of the gui.

        Arguments:
            None

        Returns:
            the application.
        """

        super().__init__()
        self.pages = {
            login: login.Login(self)
        }
        #menubar = tk.Menu(self)
        #filemenu = tk.Menu(menubar, tearoff=0)
        #filemenu.add_command(label="Edit Profile")
        #filemenu.add_command(label="Logout")
#
        #menubar.add_cascade(label="Profile", menu=filemenu)
#
        #self.config(menu=menubar)
        self.change_page(login)

    def change_page(self, new_page):
        """
        Change the currently displayed page.

        Arguments:
            newFrame -- The frame to change to
        """
        # Remove anything currently placed on the screen
        for page in self.grid_slaves():
            if page.grid_info()["column"] == 0:
                page.grid_forget()
        # Place our new page onto the screen
        self.pages[new_page].grid(row=0, column=0)


if __name__ == "__main__":
    application = App()
    application.mainloop()
