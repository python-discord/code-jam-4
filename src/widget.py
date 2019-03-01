import tkinter as tk
from configparser import ConfigParser
from . import THEME

parser = ConfigParser()
parser.read(THEME)


class SecondaryFrame(tk.Frame):
    DEFAULT = {}

    def __init__(self, *args, **kwds):
        self.DEFAULT.update(kwds)
        super().__init__(*args, **self.DEFAULT)
        if hasattr(self, 'init'):
            self.init()


class SecondaryButton(tk.Button):
    DEFAULT = {
        'height': 1,
        'width': 10
    }

    def __init__(self, *args, **kwds):
        self.DEFAULT.update(kwds)
        super().__init__(*args, **self.DEFAULT)
        if hasattr(self, 'init'):
            self.init()


class SecondaryLabel(tk.Label):
    DEFAULT = {}

    def __init__(self, *args, **kwds):
        self.DEFAULT.update(kwds)
        super().__init__(*args, **self.DEFAULT)
        if hasattr(self, 'init'):
            self.init()


class SecondaryCanvas(tk.Canvas):
    DEFAULT = {}

    def __init__(self, *args, **kwds):
        self.DEFAULT.update(kwds)
        super().__init__(*args, **self.DEFAULT)
        if hasattr(self, 'init'):
            self.init()


class PrimaryFrame(tk.Frame):
    DEFAULT = {}

    def __init__(self, *args, **kwds):
        self.DEFAULT.update(kwds)
        super().__init__(*args, **self.DEFAULT)
        if hasattr(self, 'init'):
            self.init()


class PrimaryButton(tk.Button):
    DEFAULT = {
        'height': 2,
        'width': 10
    }

    def __init__(self, *args, **kwds):
        self.DEFAULT.update(kwds)
        super().__init__(*args, **self.DEFAULT)
        if hasattr(self, 'init'):
            self.init()


class PrimaryLabel(tk.Label):
    DEFAULT = {}

    def __init__(self, *args, **kwds):
        self.DEFAULT.update(kwds)
        super().__init__(*args, **self.DEFAULT)
        if hasattr(self, 'init'):
            self.init()


class PrimaryCanvas(tk.Canvas):
    DEFAULT = {}

    def __init__(self, *args, **kwds):
        self.DEFAULT.update(kwds)
        super().__init__(*args, **self.DEFAULT)
        if hasattr(self, 'init'):
            self.init()
