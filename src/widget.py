import tkinter as tk
from configparser import ConfigParser
from . import THEME, IMAGES

parser = ConfigParser()
parser.read(THEME)


class SecondaryFrame(tk.Frame):
    DEFAULT = {
        'bg': 'gray'
    }

    def __init__(self, *args, **kwds):
        super().__init__(*args, **{**self.DEFAULT, **kwds})
        if hasattr(self, 'init'):
            self.init()


class SecondaryButton(tk.Button):
    DEFAULT = {
        'height': 1,
        'width': 10
    }

    def __init__(self, *args, **kwds):
        super().__init__(*args, **{**self.DEFAULT, **kwds})
        if hasattr(self, 'init'):
            self.init()


class SecondaryLabel(tk.Label):
    DEFAULT = {
        'justify': 'left',
        'width': 10,
        'bg': 'gray'
    }

    def __init__(self, *args, **kwds):
        super().__init__(*args, **{**self.DEFAULT, **kwds})
        if hasattr(self, 'init'):
            self.init()


class SecondaryCanvas(tk.Canvas):
    DEFAULT = {}

    def __init__(self, *args, **kwds):
        super().__init__(*args, **{**self.DEFAULT, **kwds})
        if hasattr(self, 'init'):
            self.init()


class PrimaryFrame(tk.Frame):
    DEFAULT = {
        'bg': 'black'
    }

    def __init__(self, *args, **kwds):
        super().__init__(*args, **{**self.DEFAULT, **kwds})
        if hasattr(self, 'init'):
            self.init()


class PrimaryButton(tk.Button):
    DEFAULT = {
        'height': 3,
        'width': 10
    }

    def __init__(self, *args, **kwds):
        super().__init__(*args, **{**self.DEFAULT, **kwds})
        if hasattr(self, 'init'):
            self.init()


class PrimaryLabel(tk.Label):
    DEFAULT = {
        'font': ('Courier', 25),
        'bg': 'black',
        'fg': 'gray'
    }

    def __init__(self, *args, **kwds):
        super().__init__(*args, **{**self.DEFAULT, **kwds})
        if hasattr(self, 'init'):
            self.init()


class PrimaryCanvas(tk.Canvas):
    DEFAULT = {
        'bg': 'black'
    }

    def __init__(self, *args, **kwds):
        super().__init__(*args, **{**self.DEFAULT, **kwds})
        if hasattr(self, 'init'):
            self.init()


class PrimaryCheckbutton(tk.Checkbutton):
    DEFAULT = {
        'bg': 'black'
    }
    img = IMAGES / 'checkbox.png'

    def __init__(self, *args, **kwds):
        img = tk.PhotoImage(file=self.img)
        super().__init__(*args, image=img, **{**self.DEFAULT, **kwds})
        if hasattr(self, 'init'):
            self.init()
