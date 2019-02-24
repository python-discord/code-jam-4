"""Add event page for the calendar application."""
import tkinter as tk


class AddEventPage(tk.Frame):
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
        self.title = tk.Label(self, text="Add an event", font=(30))
        self.title.grid(column=1)
        # Name
        self.name = tk.Label(self, text="Name", font=(24))
        self.name.grid(row=1, sticky="E")
        self.nameEntry = tk.Entry(self)
        self.nameEntry.grid(row=1, column=1)
        # Location
        self.location = tk.Label(self, text="Location", font=(24))
        self.location.grid(row=2, sticky="E")
        self.locationEntry = tk.Entry(self)
        self.locationEntry.grid(row=2, column=1)
        # Date
        self.date = tk.Label(self, text="Date", font=(24))
        self.date.grid(row=3, sticky="E")
        self.dateEntry = tk.Entry(self)
        self.dateEntry.grid(row=3, column=1)
        # Description
        self.description = tk.Label(self, text="Description", font=(24))
        self.description.grid(row=4, sticky="E")
        self.descriptionEntry = tk.Text(self, height=5, width=15)
        self.descriptionEntry.grid(row=4, column=1)
        # Submit Button
        if len(self.nameEntry.get()) == 0 or \
           len(self.locationEntry.get()) == 0 or \
           len(self.dateEntry.get()) == 0 or \
           len(self.descriptionEntry.get("1.0")) == 0:
            # Need some sort of UI goodness here!
            print("[AddEventPage] Not all boxes filled")
            # Break out
        self.submitBtn = tk.Button(self,
                                   text="Submit ✔",
                                   command=lambda: self.parent.dbh.addEvent(
                                            self.nameEntry.get(),
                                            self.locationEntry.get(),
                                            self.dateEntry.get(),
                                            self.descriptionEntry.get("1.0")
                                                            ))
        self.submitBtn.grid()
