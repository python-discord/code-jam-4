from tkinter import *
from PIL import Image, ImageTk

class weatherh8su:
    def __init__(self, master):
        self.master = master
        master.title("Weather h8su")
        self.create_widgets()


    def create_widgets(self):
        master = self.master
        self.glass = Image.open("pics/glass.png")
        self.glass = ImageTk.PhotoImage(self.glass)
        self.searchicon = Label(master, image=self.glass)
        self.searchicon.grid(row=0,column=0)
        self.searchbar = Entry(master, width=70)
        self.searchbar.grid(row=0,column=1)
        self.f = Frame(master, width=26, height=52)
        self.f.grid(column=2,row=1)
        self.gear = Image.open("pics/gear.png")
        self.gear = ImageTk.PhotoImage(self.gear)
        self.settings = Label(master, image=self.gear)
        self.settings.bind("<Enter>", lambda a: self.annoy())
        self.settings.bind("<Leave>", lambda a: self.deannoy())
        self.f.bind("<Leave>", lambda a: self.deannoy())
        self.settings.grid(column=2,row=0)

    def annoy(self):
        self.settings.grid(row=1)
        self.f.grid(row=0)

    def deannoy(self):
        if self.mouse_on(self.settings) or self.mouse_on(self.f):
            return
        self.settings.grid(row=0)
        self.f.grid(row=1)

    def mouse_on(self, widget):
        if self.master.winfo_containing(*self.master.winfo_pointerxy()) == widget:
            return True
        return False

root = Tk()
root.geometry("600x600")
app = weatherh8su(root)
root.mainloop()
