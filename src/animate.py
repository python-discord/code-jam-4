from __future__ import annotations

import tkinter as tk
import operator
from math import log2
from typing import NamedTuple, Callable, TypeVar, List
from enum import Flag
from dataclasses import dataclass
from functools import partialmethod


class Coord(NamedTuple):
    """
    Helper class for managing coordinate values.

    Coord overloads many of the numeric operators by mapping
    it to the x and y values individually.

    param:
        x: int -- X position.
        y: int -- Y position.

    example::

    ```
    c1 = c2 = Coord(1, 1)
    c1 + c2
    >>> Coord(2, 2)
    # For convenience, integers are accepted as well
    c1 = Coord(1, 1)
    c1 + 1  # 1 is cast to Coord(1, 1)
    >>> Coord(2, 2)
    ```

    note:

    True divide `round`s in order to remain compatible with tkinter
    coordinate values (`int`).
    """

    x: int
    y: int

    Operand = TypeVar('Operand', 'Coord', int)

    def __apply(self, op: Callable, other: Coord.Operand) -> Coord:
        if isinstance(other, int):
            other = Coord(other, other)

        x = op(self.x, other.x)
        y = op(self.y, other.y)
        return Coord(x, y)

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

    def __truediv__(self, other):
        result = self.__apply(operator.truediv, other)
        return Coord(*map(round, result))

    __add__ = partialmethod(__apply, operator.add)
    __sub__ = partialmethod(__apply, operator.sub)
    __mul__ = partialmethod(__apply, operator.mul)
    __mod__ = partialmethod(__apply, operator.mod)
    __pow__ = partialmethod(__apply, operator.pow)
    __floordiv__ = partialmethod(__apply, operator.floordiv)


class Direction(Flag):
    """
    Defines base directions.


    """
    LEFT = Coord(-1, 0)
    RIGHT = Coord(1, 0)
    UP = Coord(0, 1)
    DOWN = Coord(0, -1)

    def __mul__(self, other: int) -> Coord:
        return self.value * other

    def __add__(self, other: Direction) -> Coord:
        return self.value + other.value


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

    # def add(self, )


def vector(start: Coord, end: Coord, step: int = 60) -> List[Coord]:
    """
    Creates a list of all the Coords on a straight line from `start` to `end`.

    param:
        start: Coord -- The starting point.
        end: Coord -- The ending point.
        step: int (optional) -- The desired number of points to include. Defaults to 60.
            Actual resulting length may vary.

    return:
        List[Coord] -- All points that fall on the line from start to end.

    example::

    ```
    start = Coord(0, 0)
    end = Coord(5, 0)
    vector(start, end, 5)
    >>> [Coord(x=0, y=0), Coord(x=1, y=0), Coord(x=2, y=0), Coord(x=4, y=0)]
    ```

    note:

    The current implementation recursively finds midpoints to build the line.
    This means the resulting length may vary, due to its eager nature.
    """
    mid = start.midpoint(end)
    instep = round(step / 2)
    if instep:
        back = vector(start, mid, step=instep)
        front = vector(mid, end, step=instep)
        return back + front
    else:
        return [start]
