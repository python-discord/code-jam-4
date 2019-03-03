import configparser
import tkinter as tk
from contextlib import suppress

from .front import Front
# from .splash import Splash
from . import SETTINGS, widget


parser = configparser.ConfigParser()
parser.read(SETTINGS)


class App(tk.Tk):
    appconfig = parser['APP']

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.resizable(False, False)

        for name, val in parser['APP'].items():
            getattr(self, name)(val)

        self.frame = widget.PrimaryFrame(self)
        self.frame.pack(expand=True, fill='both')

        # self.splash = Splash(self.frame)
        # self.splash.pack(expand=True, fill='both')
        self.front = Front(self.frame)
        self.front.pack(fill='both', expand=True)

    def cleanup(self):import configparser
import tkinter as tk
from contextlib import suppress

from .view import Window, View
from .front import Front
from .splash import Splash
from . import SETTINGS


parser = configparser.ConfigParser()
parser.read(SETTINGS)


class App(tk.Tk):
    appconfig = parser['APP']

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.resizable(False, False)
        for name, val in parser['APP'].items():
            getattr(self, name)(val)

        self.window = Window(self)
        self.window.pack(expand=True, fill='both')
        self.update()

        self.splash = Splash(self)
        self.front = Front(self)
        self.front.pack(fill='both', expand=True)
        self.execution_order = iter((
            # self.splash,
            self.front,
            # self.result
        ))
        self.update()
        self.switch()

    def switch(self):
        try:
            self.update()
            if self.current is not None:
                self.current.data.cleanup()
                self.current.data.pack_forget()
                self.current.data.destroy()
            self.current = next(self.execution_order)
            self.build(self.current)
        except StopIteration:
            self.cleanup()

    def build(self, view):
        self.update()
        view.data.build()
        self.window.set_view(view)

    def cleanup(self):
        with suppress(Exception):
            self.current.cleanup()
            self.destroy()

        with suppress(Exception):
            self.front.cleanup()
            self.destroy()
