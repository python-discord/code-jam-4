"""
.. module:: Stack
    :synopsis: Class encapsulating the behavior of the stack.

.. moduleauthor:: Bryan Kok <bryan.wyern1@gmail.com>
"""
import enum


class Stack:
    """ A collection of strings/other objects """

    # if it is a collection please consider adding magic
    # methods for this (e.g. "__len__", "__iter__",...)

    class SHIFT_DIRECTION(enum.Enum):
        UP = 1
        DOWN = 2

    def __init__(self, existing_stack=[], cur_stack_pointer=None):
        # Stack is backwards???
        self._stack = existing_stack

        if cur_stack_pointer:
            self._stack_pointer = cur_stack_pointer
        else:
            # By default the stack pointer is at the top of the stack (-1 ??)
            self._stack_pointer = len(self._stack) - 1

    # this should be __iter__
    def items(self):
        return self._stack

    def items_count(self):
        return len(self._stack)

    # this should be __setitem__
    def set_current_item(self, idx):
        # What does idx relate to
        if not 0 <= idx < len(self._stack):
            raise Exception("Index is out of bounds")

        self._stack_pointer = idx

    @property
    def current_item_idx(self):
        return self._stack_pointer

    @property
    def current_item(self):
        return self._stack[self._stack_pointer] if self._stack else None

    def shift_current_item(self, shift_direction: SHIFT_DIRECTION):
        """Shifts the current item pointed to by the stack pointer up or down"""

        if self._stack_pointer <= 0 and shift_direction == Stack.SHIFT_DIRECTION.DOWN or \
                self._stack_pointer == self.items_count() - 1 \
                and shift_direction == Stack.SHIFT_DIRECTION.UP:
            return

        _temp = self._stack[self._stack_pointer]
        if shift_direction == Stack.SHIFT_DIRECTION.UP:
            self._stack[self._stack_pointer] = self._stack[self._stack_pointer + 1]
            self._stack[self._stack_pointer + 1] = _temp
            self._stack_pointer += 1

        elif shift_direction == Stack.SHIFT_DIRECTION.DOWN:
            self._stack[self._stack_pointer] = self._stack[self._stack_pointer - 1]
            self._stack[self._stack_pointer - 1] = _temp
            self._stack_pointer -= 1

    def swap_items(self, idx, target_idx):
        _temp = self._stack[idx]
        self._stack[idx] = self._stack[target_idx]
        self._stack[target_idx] = _temp

    def push_item(self, item):
        self._stack.append(item)
        if self.items_count() == 1:
            self.set_current_item(0)

        self._stack_pointer = self.items_count() - 1

    # this should be __getitem__
    def peek(self):
        if not self._stack:
            return None
        return self._stack[-1]  # if we reverse stack at start we won't have to do this

    def pop(self, index=-1):
        self._stack_pointer = max(0, self._stack_pointer - 1)

        return self._stack.pop(index)

    def clear(self):
        self._stack = []
