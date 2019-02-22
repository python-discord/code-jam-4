import tkinter as tk


class Login(tk.Frame):
    """The login page for this application."""
    def __init__(self, parent):
        """
        Initilises the login page.

        Parameters:
            parent -- the main application
        Returns:
            the Login page.
        """
        super().__init__()
        self.title = tk.Label(self, text="Plase login")
        self.username = tk.Entry(self)
        self.password = tk.Entry(self, show="*")
        self.username_label = tk.Label(self, text="Username:")
        self.password_label = tk.Label(self, text="Password:")
        self.login_button = tk.Button(self, text="Login")

        self.username.grid(row=2, column=1)
        self.password.grid(row=3, column=1)
        self.username_label.grid(row=2)
        self.password_label.grid(row=3)
        self.title.grid(row=0, column=1)
        self.login_button.grid(row=4, column=1)
        