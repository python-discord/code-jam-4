"""Calendar application for OOP tkinter."""
import tkinter as tk
from DBHandler import DBHandler


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

        self.pages[CalendarPage] = CalendarPage(self)

        self.change_page(CalendarPage)

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


class CalendarPage(tk.Frame):
    """Example page for Application."""

    eventLabels = {
        0: "ID",
        1: "Name",
        2: "Location",
        3: "Date",
        4: "Description"
    }

    def __init__(self, parent):
        """
        Initialise the Example page.

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
        # Fetch all events
        events = self.parent.dbh.fetchEvents()
        print(events)
        # Event format:
        # (ID, name, location, description)--
        for event in events:
            string = ""
            for value in event:
                string += self.eventLabels[event.index(value)] + " - "
                string += str(value) + "\n"
            eventPanel = tk.PanedWindow(self, bd=5, relief="sunken", width=600)
            eventPanel.grid()
            eventPanel.add(tk.Label(self, text=string))


if __name__ == "__main__":
    app = Application()
    app.mainloop()
