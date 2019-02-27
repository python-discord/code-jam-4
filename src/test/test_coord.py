from ..animate import Coord

coord1 = Coord(1, 1)
coord2 = Coord(1, 1)


def test_add():
    assert coord1 + coord2 == Coord(2, 2)
    assert coord1 + 1 == Coord(2, 2)


def test_sub():
    assert coord1 - coord2 == Coord(0, 0)
    assert coord1 - 1 == Coord(0, 0)


def test_mul():
    assert coord1 * coord2 == Coord(1, 1)
    assert coord1 * 1 == Coord(1, 1)


def test_mod():
    assert coord1 % coord2 == Coord(0, 0)
    assert coord1 % 1 == Coord(0, 0)


def test_pow():
    assert coord1 ** coord2 == Coord(1, 1)
    assert coord1 ** 1 == Coord(1, 1)


def test_truediv():
    assert coord1 / Coord(2, 2) == Coord(0.5, 0.5)
    assert coord1 / 2 == Coord(0.5, 0.5)


def test_floordiv():
    assert coord1 // coord2 == Coord(1, 1)
    assert coord1 // 1 == Coord(1, 1)
