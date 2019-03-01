# from .mainwindow import Tinder

# if __name__ == "__main__":
#     Tinder().start()

from .animate import Animater, Coord
import tkinter as tk

root = tk.Tk()
window = Animater(root)
rect = window.create_rectangle(
    55, 60, 70, 75
)

window.pack()

end = Coord(100, 100)
window.add_motion(rect, (end,), speed=1.9)

start = tk.Button(
    root, width=20, height=3, text='Start', command=window.start
)
start.pack()
tk.mainloop()
