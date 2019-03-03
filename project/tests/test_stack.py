"""
.. module:: test_stack.py
    :synopsis: Unit tests for the stack, the core of this app. We should have started testing earlier, eh?

.. moduleauthor:: Bryan Kok <bryan.wyern1@gmail.com>
"""
import pytest

from project.Stack import Stack


@pytest.fixture(scope='function')
def clean_stack():
    return Stack()


def test_clear(clean_stack):
    """Ensure that clear empties the stack."""
    _stack = clean_stack
    for i in range(5):
        _stack.push_item(i)

    assert (_stack.items_count() == 5)

    _stack.clear()
    assert (_stack.items_count() == 0)


def test_push_items(clean_stack):
    """Ensure that the stack retains pushed items"""

    _stack = clean_stack
    _list = [1, 2, 'a', 'b', 'c']
    for _item in _list:
        _stack.push_item(_item)

    assert (_stack.items_count() == 5)
    assert (_stack.items() == _list)
    _stack.clear()


def test_shift_item_down(clean_stack):
    """Shifting an item down should not affect order of other items in stack"""

    _stack = clean_stack
    _list = [1, 2, 'a', 'b', 'c', 3, 4, 5]
    for _item in _list:
        _stack.push_item(_item)

    _stack.set_current_item(3)  # b
    _stack.shift_current_item(Stack.SHIFT_DIRECTION.DOWN)
    assert (_stack.items() == [1, 2, 'b', 'a', 'c', 3, 4, 5])


def test_shift_item_up(clean_stack):
    """Shifting an item up should not affect order of other items in stack"""

    _stack = clean_stack
    _list = [1, 2, 'a', 'b', 'c', 3, 4, 5]
    for _item in _list:
        _stack.push_item(_item)

    _stack.set_current_item(3)  # b
    _stack.shift_current_item(Stack.SHIFT_DIRECTION.UP)
    assert (_stack.items() == [1, 2, 'a', 'c', 'b', 3, 4, 5])


def test_peek(clean_stack):
    """The top of the stack should always be returned by peek"""
    _stack = clean_stack
    for _item in [1, 2, 3]:
        _stack.push_item(_item)
        assert (_stack.peek() == _item)
