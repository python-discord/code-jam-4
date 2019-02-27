import tkinter as tk
from enum import Flag
from dataclasses import dataclass

from .coord import Coord


class Direction(Flag):
    LEFT = Coord(-1, 0)
    RIGHT = Coord(1, 0)
    UP = Coord(0, 1)
    DOWN = Coord(0, -1)


class Window(tk.Canvas):

    events = []

    def set_event(self, event: tk.EventType):
        self.bind(event, self.run)

    def run(self, event):
        pass


@dataclass
class Motion:

    canvas: tk.Canvas
    direction: Direction
    speed: int

    frames = 30






class Animate:

    def __init__(self, obj: tk.Widget):
        self.obj = obj

    def set_event(self, event: tk.EventType):
        self.bind(event, self.run)

    def add(self, )

