from __future__ import annotations

import tkinter as tk
import operator
import time
import math
import random
from typing import NamedTuple, Callable, TypeVar, Generator
from enum import Enum
from functools import partialmethod


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

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas

    def start(self):
        while self._motions:
            self.run()

    def run(self):
        for motion in self._motions.copy():
            try:
                move = next(motion)
                move()
                self.canvas.update()
            except StopIteration:
                self._motions.remove(motion)
        self.canvas.update()
        # self.canvas.after(10, self.run)

    def add(self, motion: Motion):
        self._motions.add(motion.start())

    def add_motion(self, id: int, end: Coord, **kwargs):
        motion = Motion(self.canvas, id, end, **kwargs)
        self.add(motion)

    def clear(self):
        self._motions.clear()

    @property
    def running(self):
        return bool(self._motions)


class Motion:
    def __init__(self, canvas: tk.Canvas, id: str, end: Coord, speed: float = 1):
        self.canvas = canvas
        self.id = id
        self.end = end
        self.speed = speed ** 3

    def __iter__(self):
        return self.start()

    def __key(self):
        return self.id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self):
        return isinstance(self, type(other)) and self.__key() == other.__key()

    def start(self) -> Generator[Callable]:
        """
        The entry point for generating move commands.
        """
        self.reset()
        while self.current != self.end:
            print(self.current, self.end)
            yield self.move

    def reset(self):
        self.time = time.time()
        self.beg = self.current
        self.distance = self.beg.distance(self.end)

    def move(self):
        self.canvas.move(self.id, *self.increment)
        self.canvas.update_idletasks()

    @property
    def time(self):
        return time.time() - self._time

    @time.setter
    def time(self, val):
        self._time = val

    @property
    def increment(self):
        future = self.future
        if future.distance(self.end) > self.journey:
            return self.end - self.current
        else:
            return future - self.current

    @property
    def future(self):
        mult = (self.time * self.speed) / self.distance
        return (self.end - self.beg) * mult + self.beg

    @property
    def current(self):
        return Coord(*self.canvas.coords(self.id))

    @property
    def journey(self):
        return self.current.distance(self.end)


class BounceBall(Motion):

    chaos = 3

    def kick(self, direction: Point):
        self.canvas.update()

        c1, c2 = -self.chaos, self.chaos
        chaoticx, chaoticy = random.randint(c1, c2), random.randint(c1, c2)
        self.direction = direction + Coord(chaoticx, chaoticy)
        self.end = self.direction * self.canvas.winfo_height()
        self.reset()

    @property
    def increment(self):
        bounce = self.get_bounce()
        if bounce != Coord(0, 0):
            self.kick(bounce)
        return self.future - self.current

    def get_bounce(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        bounce = Coord(0, 0)
        if x1 <= self.bound_x1:
            bounce += Direction.RIGHT
        if y1 <= self.bound_y1:
            bounce += Direction.DOWN
        if x2 >= self.bound_x2:
            bounce += Direction.LEFT
        if y2 >= self.bound_y2:
            bounce += Direction.UP
        return bounce

    @property
    def bound_x1(self):
        return self.canvas.winfo_x()

    @property
    def bound_y1(self):
        return self.canvas.winfo_y()

    @property
    def bound_x2(self):
        return self.bound_x1 + self.canvas.winfo_width()

    @property
    def bound_y2(self):
        return self.bound_y1 + self.canvas.winfo_height()


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
        if isinstance(other, Direction):
            other = other.value
        elif not isinstance(other, self.__class__):
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

    def distance(self, other: Coord) -> float:
        """
        The distance between `self` and `other`.

        param:
            other: Coord -- THe point to consider.

        return:
            int -- A numeric representation of the distance between two points.
        """
        diff = other - self
        return math.hypot(*diff)

    def flip(self):
        return Coord(0, 0) - self

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
