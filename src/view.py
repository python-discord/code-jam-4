import tkinter as tk
from typing import TypeVar
from enum import Enum

from . import widget
from .animate import Coord, Animater
from .cache import ImageTk


class ViewType(Enum):
    IMAGE = 'IMAGE'
    WIDGET = 'WIDGET'


T = TypeVar('T', ImageTk.PhotoImage, tk.Widget)


@dataclass
class View:
    data: T
    viewtype: ViewType


class Window(widget.PrimaryCanvas):
    animation_speed = 4
    current = None
    views = {}

    def init(self):
        self.animater = Animater(self)

    def __coord(self, id):
        return Coord(*self.coords(id)[:2])

    def __set_image(self, view: ImageTk.PhotoImage, coord: Coord):
        return self.create_image(
            coord, image=view, anchor='nw'
        )

    def __set_widget(self, view: tk.Widget, coord: Coord):
        return self.create_window(
            coord, window=view, anchor='nw'
        )

    def __set(self, view, coord, viewtype):
        if viewtype == 'image':
            wid = self.__set_image(view, coord)
        else:
            wid = self.__set_widget(view, coord)
        self.views[view] = wid
        return wid

    def set_view(self, view: tk.Widget, viewtype='image'):
        self.current = view
        self.__set(self.current, self.origin, viewtype)

    def move_view(self, wid, end):
        self.animater.add_motion(
            wid, end, speed=self.animation_speed
        )

    def move_in(self, view, direction: Direction, viewtype='image'):
        distance = self.get_distance(direction)
        start = self.origin + distance
        wid = self.__set(view, start, viewtype)
        self.move_view(wid, self.origin)
        return wid

    def move_out(self, view, direction, viewtype='image'):
        wid = self.views[view]
        distance = self.get_distance(direction)
        end = self.origin + distance
        self.move_view(wid, end)
        del self.views[view]

    def change_view(self, view: tk.Widget, direction: Direction, viewtype='image'):
        if not isinstance(direction, Direction):
            direction = Direction[direction.upper()]  # Cast string for convenience
        self.animater.clear()

        self.move_out(self.current, direction, viewtype=viewtype)
        self.move_in(view, direction.flip(), viewtype=viewtype)

        self.animater.start()
        self.current = view

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
    def origin(self):
        return Coord(0, 0)
