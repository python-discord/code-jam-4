from __future__ import annotations

import tkinter as tk
from typing import TypeVar
from enum import Enum
from PIL import ImageTk

from . import widget
from .animate import Coord, Animater, Direction


class Window(widget.PrimaryCanvas):
    animation_speed = 4
    current = None
    views = {}

    def init(self):
        self.animater = Animater(self)

    def __coord(self, id):
        return Coord(*self.coords(id)[:2])

    def __set(self, view: View, coord: Coord):
        wid = view.draw(coord, anchor='nw')
        self.views[view] = wid
        return wid

    def set_view(self, view: View):
        self.current = view
        self.__set(self.current, self.origin)

    def move_view(self, view: View, end: Coord):
        wid = self.views.get(view)
        if wid is not None:
            self.animater.add_motion(
                wid, end, speed=self.animation_speed
            )

    def move_in(self, view: View, direction: Direction):
        distance = self.get_distance(direction)
        start = self.origin + distance
        wid = self.__set(view, start)
        self.move_view(view, self.origin)
        return wid

    def move_out(self, view: View, direction: Direction):
        distance = self.get_distance(direction)
        end = self.origin + distance
        self.move_view(view, end)
        del self.views[view]

    def change_view(self, view: View, direction: Direction = None):
        if direction is None:
            self.set_view(view)
            return
        if not isinstance(direction, Direction):
            direction = Direction[direction.upper()]  # Cast string for convenience
        self.animater.clear()

        last = self.current
        self.current = view
        self.move_in(self.current, direction.flip())
        self.move_out(last, direction)

        self.animater.start()

    def get_distance(self, direction: Direction):
        if not isinstance(direction, Direction):
            direction = Direction[direction.upper()]  # Cast string for convenience

        if direction in (Direction.UP, Direction.DOWN):
            return direction * Coord(0, self.winfo_height())
        elif direction in (Direction.LEFT, Direction.RIGHT):
            return direction * Coord(self.winfo_width(), 0)
        else:
            raise NotImplementedError

    @property
    def active(self):
        return self.animater.running

    @property
    def origin(self):
        return Coord(self.canvasx(0), self.canvasy(0))


class DrawType(Enum):
    IMAGE = 'create_image'
    WIDGET = 'create_window'
    TEXT = 'create_text'


class View:

    def __init__(self, window: Window, **kwds):
        self.window = window
        self.kwds = kwds
        self.drawtype = self.data = None
        for k, v in self.kwds.items():
            k = k.upper()
            if hasattr(DrawType, k):
                self.drawtype = DrawType[k]
                self.data = v
        if self.drawtype is None:
            raise NotImplementedError

    def draw(self, *args, **kwds):
        fn = getattr(self.window, self.drawtype.value)
        return fn(*args, **{**self.kwds, **kwds})
