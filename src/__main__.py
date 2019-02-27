import tkinter as tk

from .animate import Motion, Animater, Coord, Direction

root = tk.Tk()

window = Animater(root)
window.pack()

c1 = Coord(50, 55)
c2 = Coord(60, 65)
rect = window.create_rectangle(c1, c2)

end = c1 + Direction.RIGHT * 50
end2 = end + Direction.DOWN * 50
end3 = end2 + (Direction.UP + Direction.LEFT) * 50

animation = Motion(window, rect, (end, end2, end3), speed=1)

window.add_motion(animation)
window.add_event('<B1-Motion>')

root.mainloop()
