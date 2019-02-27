import tkinter as tk

from .animate import Window

root = tk.Tk()

w = Window(root)
w.pack()

tk.mainloop()
