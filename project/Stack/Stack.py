"""
.. module:: Stack
    :synopsis: Class encapsulating the behavior of the stack.

.. moduleauthor:: Bryan Kok <bryan.wyern1@gmail.com>
"""
import enum


class Stack:
    class SHIFT_DIRECTION(enum.Enum):
        UP: 1
        DOWN: 2

    def __init__(self, existing_stack=None, cur_stack_pointer=None):
        if existing_stack:
            self._stack = existing_stack
        else:
            self._stack = []

        if cur_stack_pointer:
            self._stack_pointer = cur_stack_pointer
        else:
            # By default the stack pointer is at the top of the stack
            self._stack_pointer = len(self._stack) - 1

    def items(self):
        return self._stack

    def set_current_item(self, idx):
        if not 0 <= idx < len(self._stack):
            raise Exception("Index is out of bounds")

        self._stack_pointer = idx

    def shift_current_item(self, idx, shift_direction: SHIFT_DIRECTION):
        _temp = self._stack[self._stack_pointer]
        if shift_direction == Stack.SHIFT_DIRECTION.UP:
            self._stack[idx] = self._stack[idx + 1]
            self._stack[idx + 1] = _temp

        elif shift_direction == Stack.SHIFT_DIRECTION.DOWN:
            self._stack[idx] = self._stack[idx - 1]
            self._stack[idx - 1] = _temp

    def swap_items(self, idx, target_idx):
        _temp = self._stack[idx]
        self._stack[idx] = self._stack[target_idx]
        self._stack[target_idx] = _temp

    def push_item(self, item):
        self._stack.append(item)

    def peek(self):
        if not self._stack:
            return None
        return self._stack[-1]

    def pop(self):
        return self._stack.pop()

    def clear(self):
        self._stack = []
