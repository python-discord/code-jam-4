"""Calendar application for OOP tkinter."""
import tkinter as tk
from DBHandler import DBHandler
from pages.addeventpage import AddEventPage
from pages.calendarpage import CalendarPage
from pages.loginpage import LoginPage


class Application(tk.Tk):
    """Application class inheriting from tk.Tk."""

    def __init__(self):
        """
        Initialise the Application class.

        Arguments:
            None
        Returns:
            None
        """
        self.dbh = DBHandler()
        super().__init__()

        self.create_pages()

    def create_pages(self):
        """
        Create the pages used inside the application.

        Arguments:
            None
        Returns:
            None
        """
        self.pages = {}

        self.pages[AddEventPage] = AddEventPage(self)

        self.pages[AddEventPage] = AddEventPage(self)

        self.pages[CalendarPage] = CalendarPage(self)

        self.pages[LoginPage] = LoginPage(self)

        self.change_page(LoginPage)

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
    app = Application()
    app.mainloop()
