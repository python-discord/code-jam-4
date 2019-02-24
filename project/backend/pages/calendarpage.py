"""Main page for the calendar application."""
import tkinter as tk
from pages.addeventpage import AddEventPage


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
        # Create an add event button
        self.addEventBtn = tk.Button(self,
                                     text="[+] Add event",
                                     command=lambda: self.parent.change_page(
                                                                AddEventPage
                                                                    ))
        self.addEventBtn.grid()
        # Fetch all events
        events = self.parent.dbh.fetchEvents()
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
