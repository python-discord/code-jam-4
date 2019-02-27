from __future__ import annotations

import tkinter as tk
import operator
from typing import NamedTuple, Callable, TypeVar, List, Generator, Tuple
from contextlib import suppress
from more_itertools import chunked
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


class Animater(tk.Canvas):
    """
    Inherits Canvas. Manager for executing animation move commands.
    Currently only event base animations are supported.

    example::

    ```
    motion = Motion(...)
    window = Animator(...)
    window.add_motion(motion)
    window.add_event('<Enter>')
    ```
    """
    motions = []

    def add_event(self, event: tk.EventType):
        self.bind(event, self.run)

    def run(self, event):
        active = []
        for motion in self.motions:
            with suppress(StopIteration):
                moves = next(motion)
                for move in moves:
                    move()
                    self.update_idletasks()
                active.append(motion)
        self.motions = active

    def add_motion(self, motion: Motion):
        self.motions.append(iter(motion))


@dataclass
class Motion:
    """
    Defines the movements derived from the given vector.
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

    steps = 60
    speed: int = 1

    def start(self) -> Generator[Generator[Callable]]:
        """
        The entry point for generating move commands.
        """
        move = partial(self.canvas.move, self.id)

        def frame(points: List, last: Coord) -> Generator[Callable]:
            for point in points:
                offset = point - last
                yield partial(move, *offset)
                last = point

        for end in self.endpoints:
            start = Coord(*self.canvas.coords(self.id)[:2])
            vec = vector(start, end, self.steps)

            last = vec[0]
            for points in chunked(vec, self.speed):
                yield frame(points, last)
                last = points[-1]

    def __iter__(self):
        return self.start()


def vector(start: Coord, end: Coord, step: int = 60) -> List[Coord]:
    """
    Creates a list of all the Coords on a straight line from `start` to `end` (inclusive).

    param:
        start: Coord -- The starting point.
        end: Coord -- The end point.
        step: int (optional) -- The desired number of points to include. Defaults to 60.
            Actual resulting length may vary.

    return:
        List[Coord] -- All points that fall on the line from start to end.

    example::

    ```
    start = Coord(0, 5)
    end = Coord(5, 0)
    vector(start, end, 5)  # ends up being 8
    >>> [
        Coord(x=0, y=5), Coord(x=1, y=4), Coord(x=1, y=4),
        Coord(x=2, y=2), Coord(x=2, y=2), Coord(x=4, y=1),
        Coord(x=4, y=1), Coord(x=5, y=0)
        ]
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
        return [start, end]
