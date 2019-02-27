import tkinter as tk

from .animate import vector, Coord

start = Coord(0, 0)
end = Coord(120, 0)

result = vector(start, end, 64)
print(len(result), result)
