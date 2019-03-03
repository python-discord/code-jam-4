import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import hashlib


def hashPassword(password):
    """Hash a password using sha512."""
    return hashlib.sha512(password.encode()).hexdigest()


class Register:
    def __init__(self, db, windowTitle="REGISTER"):
        self.db = db

        self.windowTitle = windowTitle
        # Create a window.
        self.window = tk.Toplevel()

        # Set window variables.
        self.window.resizable(0, 0)
        self.window.title(self.windowTitle)
        self.window.geometry("196x290")

        # Create Labels
        self.notificationBox = tk.Label(
            self.window, width=19, height=2,
            font=("Helvetica", "12", "bold", "italic"), text=self.windowTitle)
        self.notificationBox.grid(row=0, column=0, pady=5)
        tk.Label(self.window, width=18, height=1, font=("Helvetica", "10"),
                 text="Username").grid(row=1, column=0, pady=5)
        self.userNameEntry = ttk.Entry(self.window, width=18)
        self.userNameEntry.grid(row=2, column=0)
        tk.Label(self.window, width=18, height=1, font=("Helvetica", "10"),
                 text="Password").grid(row=3, column=0, pady=5)
        self.passwordEntryFirst = ttk.Entry(self.window, width=18, show="*")
        self.passwordEntryFirst.grid(row=4, column=0)
        tk.Label(self.window, width=18, height=1, font=("Helvetica", "10"),
                 text="Confirm Password").grid(row=5, column=0, pady=5)
        self.passwordEntrySecond = ttk.Entry(self.window, width=18, show="*")
        self.passwordEntrySecond.grid(row=6, column=0)

        ttk.Button(self.window, width=18, text="Register",
                   command=self.attemptCreate).grid(row=7, column=0, pady=10)
        ttk.Button(self.window, width=18, text="Cancel",
                   command=self.closeWindow).grid(row=8, column=0)
        # Bind the create function to the return key.
        self.window.bind("<Return>", self.attemptCreate)
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.window.grab_release())
        self.userNameEntry.focus_set()

    def resetNotification(self):
        self.notificationBox["text"] = self.windowTitle

    def attemptCreate(self, event=None):
        failReason = None
        username = self.userNameEntry.get().lower()
        password = self.passwordEntryFirst.get()
        if password != self.passwordEntrySecond.get():
            failReason = "Password Mismatch"
        elif password == "":
            failReason = "No password entered."
        elif (len(password) < 8) or (password.lower() == password):
            failReason = "Password does not\nmeet requirements."
        elif (len(username) < 5):
            failReason = "Username must be at\nleast 5 characters"
        else:
            password = hashPassword(password)
            result = self.db.addUser(username, password)
            if not result:
                failReason = "User already exists"
        if failReason is not None:
            self.notificationBox["text"] = failReason
            self.userNameEntry.delete(0, tk.END)
            self.passwordEntryFirst.delete(0, tk.END)
            self.passwordEntrySecond.delete(0, tk.END)
            self.window.after(1500, self.resetNotification)
        else:
            self.name = username
            self.loggedIn = True
            self.type = "user"
            mb.showinfo(self.windowTitle, "User successfully created.")
            self.window.grab_release()
            self.window.destroy()

    def closeWindow(self):
        self.window.grab_release()
        self.window.destroy()


class Login:
    def __init__(self, db, windowTitle="LOGIN"):

        self.db = db
        # Create user variables
        self.loggedIn = False

        self.windowTitle = windowTitle
        # Create a login window.
        self.window = tk.Toplevel()
        # Set login screen variables.
        self.window.resizable(0, 0)
        self.window.title("Login")
        self.window.geometry("186x220")
        # Create labels.
        self.notificationBox = tk.Label(
            self.window, width=18, height=1,
            font=("Helvetica", "12", "bold", "italic"),
            text=self.windowTitle, anchor="center")
        self.notificationBox.grid(row=0, column=0, pady=5)
        tk.Label(self.window, width=18, height=1, font=("Helvetica", "10"),
                 text="Username").grid(row=1, column=0, pady=5)
        self.userNameEntry = ttk.Entry(self.window, width=18)
        self.userNameEntry.grid(row=2, column=0)
        tk.Label(self.window, width=18, height=1, font=("Helvetica", "10"),
                 text="Password").grid(row=3, column=0, pady=5)
        self.passwordEntry = ttk.Entry(self.window, width=18, show="*")
        self.passwordEntry.grid(row=4, column=0)

        ttk.Button(self.window, width=18, text="Login",
                   command=self.attemptLogin).grid(row=5, column=0, pady=10)

        ttk.Button(self.window, width=18, text="Cancel",
                   command=self.closeWindow).grid(row=6, column=0)

        # Bind button to window
        self.window.bind("<Return>", self.attemptLogin)
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW",
                             lambda: self.window.grab_release())
        self.userNameEntry.focus_set()

    def resetNotification(self):
        self.notificationBox["text"] = self.windowTitle

    def attemptLogin(self, event=None):
        username = self.userNameEntry.get().lower().strip()
        password = hashPassword(self.passwordEntry.get())
        result = self.db.tryLogin(username, password)
        if result is not True:
            self.passwordEntry.delete(0, tk.END)
            self.notificationBox["text"] = "Login Failed"
            self.window.after(1500, self.resetNotification)
        else:
            self.loggedIn = True
            self.window.grab_release()
            self.window.destroy()

    def closeWindow(self):
        self.window.grab_release()
        self.window.destroy()
