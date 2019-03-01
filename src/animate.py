from __future__ import annotations

import tkinter as tk
import operator
import time
from . import widget
from typing import NamedTuple, Callable, TypeVar, Generator, Tuple
from enum import Enum
from dataclasses import dataclass
from functools import partialmethod, partial


class Coord(NamedTuple):
    """
    Helper class for managing coordinate values.

    Coord overloads many of the numeric operators by mapping
    it to the x and y values individually.

    param:
        x: float -- X position.
        y: float -- Y position.

    example::

    ```
    c1 = c2 = Coord(1, 1)
    c1 + c2
    >>> Coord(2, 2)
    # For convenience, numbers are accepted as well
    c1 = Coord(1, 1)
    c1 + 1  # 1 is cast to Coord(1, 1)
    >>> Coord(2, 2)
    ```
    """

    x: float
    y: float

    Operand = TypeVar('Operand', 'Coord', float)

    def __apply(self, op: Callable, other: Coord.Operand) -> Coord:
        if not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        if isinstance(other, Direction):
            other = other.value

        x = op(self.x, other.x)
        y = op(self.y, other.y)
        return self.__class__(x, y)

    def midpoint(self, other: Coord) -> Coord:
        """
        The Coord that is equal distance from `self` and `other`.

        param:
            other: Coord -- The point to consider.

        return:
            Coord -- The resulting coordinate.
        """
        return (self + other) / 2

    def distance(self, other: Coord) -> int:
        """
        The Manhattan distance between `self` and `other`.

        param:
            other: Coord -- THe point to consider.

        return:
            int -- A numeric representation of the distance between two points.
        """
        dist = map(abs, other - self)
        return sum(dist)

    __add__ = partialmethod(__apply, operator.add)
    __sub__ = partialmethod(__apply, operator.sub)
    __mul__ = partialmethod(__apply, operator.mul)
    __mod__ = partialmethod(__apply, operator.mod)
    __pow__ = partialmethod(__apply, operator.pow)
    __floordiv__ = partialmethod(__apply, operator.floordiv)
    __truediv__ = partialmethod(__apply, operator.truediv)


class Direction(Enum):
    """
    Defines base directions. Can be used to create Coords relative
    to a direction.

    example::

    ```
    start = Coord(1, 1)
    end = start + (Direction.LEFT * 20)
    end
    >>> Coord(x=-19, y=1)
    """
    LEFT = Coord(-1, 0)
    RIGHT = Coord(1, 0)
    UP = Coord(0, -1)
    DOWN = Coord(0, 1)

    def __mul__(self, other: int) -> Coord:
        return self.value * other

    def __add__(self, other: Direction) -> Coord:
        if isinstance(other, self.__class__):
            return self.value + other.value
        else:
            return self.value + other


class Animater:
    """
    Manager for executing animations.

    example::

    ```
    motion = Motion(...)
    window = Animater(...)
    window.add_motion(motion)
    ```
    """
    _motions = set()
    fps = 60

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas

    def start(self):
        while self._motions:
            time.sleep(1/self.fps)
            self.run()

    def run(self):
        for motion in self._motions:
            try:
                next(motion)()
            except StopIteration:
                self._motions.remove(motion)
                break

    def add(self, motion: Motion):
        self._motions.add(iter(motion))

    def add_motion(self, id: int, end: Coord, **kwargs):
        motion = Motion(self.canvas, id, (end,), **kwargs)
        self.add(motion)

    def clear(self):
        self._motions.clear()


@dataclass
class Motion:
    """
    Defines the movements derived from a generated vector.
    The result is a two dimensional generator: the first dimension yields
    a "frame" generator, which in turn yields move commands. This structure allows
    for different `speed`s of motion, as the length of the second
    dimension is determined by `speed`. In other words, the `speed` determines
    how many movements occur in one frame.

    param:
        canvas: tk.Canvas -- The parent canvas to issue the move command with.
        id: int -- The id of the widget to be animated.
        endpoints: Tuple[Coord] -- The final position(s) of the widget. Multiple positions allow for
            more intricate pathing.
        speed: int (optional) -- The multipler for move commands per frame.
            Defaults to 1.

    example::

    ```
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
    ```
    """
    canvas: tk.Canvas
    id: int
    endpoints: Tuple[Coord]

    speed: int = 1

    def start(self) -> Generator[Callable]:
        """
        The entry point for generating move commands.
        """
        move = partial(self.canvas.move, self.id)

        def frame(increment: Coord, count: int):
            for _ in range(count):
                move(*increment)
                self.canvas.master.update_idletasks()

        for end in self.endpoints:
            start = Coord(*self.canvas.coords(self.id)[:2])
            steps = round(start.distance(end) / self.speed)
            frames = round(steps / self.speed)
            increment = (end - start) / steps

            for _ in range(frames):
                yield partial(frame, increment, round(steps / frames))

    def __iter__(self):
        return self.start()

    def __key(self):
        return self.id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self):
        return isinstance(self, type(other)) and self.__key() == other.__key()


class Window(widget.PrimaryCanvas):
    animation_speed = 2
    _current = None

    def init(self):
        self.animater = Animater(self)

    def __coord(self, id):
        return Coord(*self.coords(id)[:2])

    def clear(self):
        if self._current is not None:
            self.delete(self._current)
            self.update()

    def set_view(self, view: tk.Widget):
        self.clear()
        self._current = self.create_window(self.origin, window=view)

    def change_view(self, view: tk.Widget, direction: Direction):
        if not isinstance(direction, Direction):
            direction = Direction[direction.upper()]  # Cast string for convenience

        if direction in (Direction.UP, Direction.DOWN):
            edge = self.winfo_screenheight()
        elif direction in (Direction.LEFT, Direction.RIGHT):
            edge = self.winfo_screenwidth()
        else:
            raise NotImplementedError

        pos = self.__coord(self._current)
        end = pos + edge
        beg = pos - edge
        wid = self.create_window(beg, window=view)

        self.animater.clear()
        self.animater.add_motion(self._current, end, speed=self.animation_speed)
        self.animater.add_motion(wid, self.origin, speed=self.animation_speed)

        self.animater.start()
        self._current = wid

    @property
    def origin(self):
        return Coord(0, 0)
