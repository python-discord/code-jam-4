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
        self.switch()

    def switch(self):
        # self.splash.pack_forget()
        self.front = Front(self.frame)
        self.front.pack(fill='both', expand=True)


    def cleanup(self):
        self.front.cleanup()
        self.destroy()