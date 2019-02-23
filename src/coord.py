from __future__ import annotations

import operator
from typing import NamedTuple, Callable, TypeVar
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

    def __truediv__(self, other):
        result = self.__apply(operator.truediv, other)
        return Coord(*map(round, result))

    __add__ = partialmethod(__apply, operator.add)
    __sub__ = partialmethod(__apply, operator.sub)
    __mul__ = partialmethod(__apply, operator.mul)
    __mod__ = partialmethod(__apply, operator.mod)
    __pow__ = partialmethod(__apply, operator.pow)
    __floordiv__ = partialmethod(__apply, operator.floordiv)
