from __future__ import annotations

import operator
from typing import NamedTuple, Callable, TypeVar
from functools import partialmethod


class Coord(NamedTuple):
    """
    Helper class for managing coordinate values.

    Coord overloads many of the numeric operators by applying
    it to the x and y value.

    param:
        x: float -- X position.
        y: float -- Y position.

    Example::

    ```
    c1 = c2 = Coord(1, 1)
    c1 + c2
    >>> Coord(2, 2)
    # For convenience, integers are accepted as well
    c1 = Coord(1, 1)
    c1 + 1  # 1 is cast to Coord(1, 1)
    >>> Coord(2, 2)
    ```
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

    @property
    def midpoint(self) -> Coord:
        return self // Coord(2, 2)

    __add__ = partialmethod(__apply, operator.add)
    __sub__ = partialmethod(__apply, operator.sub)
    __mul__ = partialmethod(__apply, operator.mul)
    __mod__ = partialmethod(__apply, operator.mod)
    __pow__ = partialmethod(__apply, operator.pow)
    __truediv__ = partialmethod(__apply, operator.truediv)
    __floordiv__ = partialmethod(__apply, operator.floordiv)
