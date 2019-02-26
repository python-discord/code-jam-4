from typing import Callable


class Event:
    """
    This class represents an event emitter to which callbacks can be assigned.

    Example:
        def test_callback(value):
            print(value)

        new_event = Event()
        new_event.add_callback(test_callback)
        new_event('test input')

        # This will output 'test input'
    """

    def __init__(self):
        self.callbacks = set()

    def add_callback(self, callback: Callable):
        self.callbacks.add(callback)

    def take_callback(self, callback: Callable):
        self.callbacks.remove(callback)

    def __call__(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(*args, **kwargs)
