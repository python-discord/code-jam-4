"""Login page for the calendar application."""
import tkinter as tk


class LoginPage(tk.Frame):
    """Page where you can add events to the calendar."""

    def __init__(self, parent):
        """
        Initialise the Add Event page.

        Arguments:
            None
        Returns:
            None
        """
        super().__init__()
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        """
        Create the pages widgets.

        Arguments:
            None
        Returns:
            None
        """
        self.title = tk.Label(self, text="Please log-in", font=(24))
        self.title.grid(column=1)
        self.usernameLabel = tk.Label(self, text="Username")
        self.usernameLabel.grid(row=1, sticky="E")
        self.passwordLabel = tk.Label(self, text="Password")
        self.passwordLabel.grid(row=2, sticky="E")
        self.usernameEntry = tk.Entry(self)
        self.usernameEntry.grid(row=1, column=1)
        self.passwordEntry = tk.Entry(self, show="*")
        self.passwordEntry.grid(row=2, column=1)
        self.loginButton = tk.Button(self,
                                     text="Login",
                                     command=lambda:
                                     self.parent.dbh.tryLogin(self.usernameEntry.get(),
                                                              self.passwordEntry.get()))
        self.loginButton.grid(row=4, column=1)
