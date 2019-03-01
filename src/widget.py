import tkinter as tk
from configparser import ConfigParser

from . import THEME

parser = ConfigParser()
parser.read(THEME)


class MetaWidget(type):
    DEFAULTS = {}

    def __new__(cls, name, bases, namespace, **kwds):
        for base in (cls,) + bases:
            if hasattr(base, 'THEME'):
                theme = parser[base.THEME]
                kwds.update(theme)
                break

        kwds.update(cls.DEFAULTS)
        return super().__new__(cls, name, bases, namespace, **kwds)


class Base(metaclass=MetaWidget):
    THEME = 'base'

    def __init__(self, cls, *args, **kwds):
        cls.__init__(*args, **kwds)
        if hasattr(self, 'init'):
            self.init()


class Secondary(Base):
    THEME = 'secondary'


class Primary(Base):
    THEME = 'primary'


class SecondaryFrame(tk.Frame, Secondary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'init'):
            self.init()


class SecondaryButton(tk.Button, Secondary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'init'):
            self.init()


class SecondaryLabel(tk.Label, Secondary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'init'):
            self.init()


class SecondaryCanvas(tk.Canvas, Secondary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'init'):
            self.init()


class PrimaryFrame(tk.Frame, Primary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'init'):
            self.init()


class PrimaryButton(tk.Button, Primary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'init'):
            self.init()


class PrimaryLabel(tk.Label, Primary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'init'):
            self.init()


class PrimaryCanvas(tk.Canvas, Primary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'init'):
            self.init()
