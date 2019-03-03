"""Event viewer specific class."""
import tkinter as tk


def retag(tag, *args):
    '''Add the given tag as the first bindtag for every widget passed in'''
    for widget in args:
        widget.bindtags((tag,) + widget.bindtags())


class EventViewer(tk.Frame):
    """Shows all event information in a single frame."""

    eventLabels = {
        0: "ID",
        1: "Name",
        2: "Location",
        3: "Date",
        4: "Description"
    }

    def __init__(self, parent):
        """Initialise the Event Viewer class."""
        super().__init__(parent)

        self.canvas = tk.Canvas(self)
        self.display_frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", width=20,
                                      command=self.canvas.yview)
        self.canvas.configure(
            yscrollcommand=self.scrollbar.set)

        self.grid_rowconfigure(0, weight=100)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0)
        self.canvas.create_window(
            (240, 0),
            window=self.display_frame,
            anchor="n")

        self.display_frame.bind("<Configure>", self.scrollMove)
        self.display_frame.grid_columnconfigure(0, weight=1000)
        self.events = {}

    def scrollMove(self, event):
        """Update canvas information from scrollbar movement."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),
                              width=480, height=450)

    def add_event(self, event):
        """Add a new event to the viewer."""
        event_frame = Event(self.display_frame, event)
        event_frame.grid(column=0, pady=5, padx=5)

        self.events.update({event: event_frame})


class EventPopup(tk.Toplevel):
    def __init__(self, parent, event):
        super().__init__(parent)
        self.parent = parent
        self.event = event

        self.create_widgets()

    def create_widgets(self):
        self.title = tk.Label(self, text="Are you sure you wish to delete this event?",
                              font=("Helvetica", 15, "bold italic"))
        self.title.grid(row=0, column=0, pady=5)

        self.event_view = Event(self, self.event)
        self.event_view.grid(row=5, column=0, padx=5, pady=5)

        self.yes = tk.Button(self, text="YES", command=self.delete_event)
        self.yes.grid(row=10, column=0, padx=(0, 50), pady=5)

        self.no = tk.Button(self, text="NO", command=self.close_window)
        self.no.grid(row=10, column=0, padx=(50, 0), pady=5)

    def delete_event(self):
        # Insert magic to delete
        self.close_window()

    def close_window(self):
        self.destroy()


class Event(tk.Frame):
    eventLabels = {
        0: "ID",
        1: "Name",
        2: "Location",
        3: "Date",
        4: "Description"
    }

    def __init__(self, parent, event):
        super().__init__(parent)
        self.parent = parent
        self.event = event

        self.config(relief=tk.GROOVE, borderwidth=3)

        self.create_widgets()

        self.bind("<Double-Button-1>", self.show_event)

    def create_widgets(self):
        for key, name in self.eventLabels.items():
            widget = tk.Label(
                self,
                text=name + " - " + str(self.event[key]))
            retag(self, widget)
            widget.pack()

    def show_event(self, event):
        EventPopup(self, self.event)
