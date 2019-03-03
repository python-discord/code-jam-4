from __future__ import annotations

import tkinter as tk
import operator
import time
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

    def flip(self):
        return Direction(Coord(0, 0) - self.value)


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
            complete = self.run(self._motions.copy())
            self._motions -= complete
            time.sleep(1/self.fps)

    def run(self, frame):
        done = set()
        for motion in frame:
            if not self.running:
                break
            try:
                next(motion)()
                self.canvas.update()
            except StopIteration:
                done.add(motion)
        self.canvas.update()
        return done

    def add(self, motion: Motion):
        self._motions.add(iter(motion))

    def add_motion(self, id: int, end: Coord, **kwargs):
        motion = Motion(self.canvas, id, (end,), **kwargs)
        self.add(motion)

    def clear(self):
        self._motions.clear()

    @property
    def running(self):
        return bool(self._motions)


@dataclass
class Motion:
    """

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

        def frame(increment: Coord, count: int = 1):
            for _ in range(count):
                move(*increment)
                self.canvas.master.update_idletasks()

        for end in self.endpoints:
            start = self.current
            steps = round(start.distance(end) / self.speed)
            frames = round(steps / self.speed)
            increment = (end - start) / steps

            for _ in range(frames):
                yield partial(frame, increment, round(steps / frames))
            buffer = end - self.current
            yield partial(frame, buffer)

    @property
    def current(self):
        return Coord(*self.canvas.coords(self.id)[:2])

    def __iter__(self):
        return self.start()

    def __key(self):
        return self.id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self):
        return isinstance(self, type(other)) and self.__key() == other.__key()
