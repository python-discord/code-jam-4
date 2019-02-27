import tkinter as tk

from .animate import vector, Coord

start = Coord(0, 5)
end = Coord(5, 0)

result = vector(start, end, 5)
print(len(result), result)
