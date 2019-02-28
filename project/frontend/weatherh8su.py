import tkinter as tk
from PIL import Image, ImageTk
from os.path import realpath


class weatherh8su:
    def __init__(self, master):
        self.master = master
        master.title("Weather h8su")
        self.create_widgets()

    def create_widgets(self):
        self.directory = "\\".join(realpath(__file__)
                                   .split("\\")[:-3]) + "\\data\\"
        self.topframe = tk.Frame(self.master)
        self.topframe.pack()
        self.glass = Image.open(f"{self.directory}glass.png")
        self.glass = ImageTk.PhotoImage(self.glass)
        self.searchicon = tk.Label(self.topframe, image=self.glass)
        self.searchicon.grid(row=0, column=0)
        self.searchbar = tk.Entry(self.topframe, width=70)
        self.searchbar.grid(row=0, column=1)
        self.f = tk.Frame(self.topframe, width=26, height=30)
        self.f.grid(column=2, row=1)
        self.gear = Image.open(f"{self.directory}gear.png")
        self.gear = ImageTk.PhotoImage(self.gear)
        self.settings = tk.Label(self.topframe, image=self.gear)
        self.settings.bind("<Enter>", lambda a: self.annoy())
        self.settings.bind("<Leave>", lambda a: self.deannoy())
        self.f.bind("<Leave>", lambda a: self.deannoy())
        self.settings.grid(column=2, row=0)
        self.todaysframe = tk.Frame(self.master)
        self.todaysframe.pack(anchor="w")
        self.todayslabel = tk.Label(self.todaysframe, text="TODAY:",
                                    font=(None, 30), height=2, anchor="s")
        self.todayslabel.pack()
        self.todayscontent = tk.Label(
            self.todaysframe, text="content\nhere", font=(None, 15))
        self.todayscontent.pack(side=tk.LEFT)
        self.tomorrowsframe = tk.Frame(self.master)
        self.tomorrowsframe.pack(anchor="w", pady=30)
        self.tomorrowslabel = tk.Label(
            self.tomorrowsframe, text="TOMORROW:",
            font=(None, 30), height=2, anchor="s")
        self.tomorrowslabel.pack()
        self.tomorrowscontent = tk.Label(
            self.tomorrowsframe, text="content\nhere", font=(None, 15))
        self.tomorrowscontent.pack(side=tk.LEFT)

    def annoy(self):
        self.settings.grid(row=1)
        self.f.grid(row=0)

    def deannoy(self):
        if self.mouse_on(self.settings) or self.mouse_on(self.f):
            return
        self.settings.grid(row=0)
        self.f.grid(row=1)

    def mouse_on(self, widget):
        if self.master.winfo_containing(
                *self.master.winfo_pointerxy()) == widget:
            return True
        return False


root = tk.Tk()
app = weatherh8su(root)
root.mainloop()
