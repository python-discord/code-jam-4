"""Event viewer specific class."""
import tkinter as tk


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
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.grid_rowconfigure(0, weight=100)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0)
        self.canvas.create_window((240, 0), window=self.display_frame, anchor="n")

        self.display_frame.bind("<Configure>", self.scrollMove)
        self.display_frame.grid_columnconfigure(0, weight=1000)

        self.events = {}

    def scrollMove(self, event):
        """Update canvas information from scrollbar movement."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),
                              width=480, height=450)

    def add_event(self, event):
        """Add a new event to the viewer."""
        event_frame = tk.Frame(self.display_frame,
                               relief=tk.GROOVE, borderwidth=3)
        event_frame.grid(column=0, pady=5, padx=5)

        self.events.update({event: event_frame})

        for key, name in self.eventLabels.items():
            widget = tk.Label(event_frame, text=name+" - "+str(event[key]))
            widget.pack()
