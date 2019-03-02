import configparser
import tkinter as tk
from pygame import mixer

from .front import Front
from .view import Window, View
from . import SETTINGS


parser = configparser.ConfigParser()
parser.read(SETTINGS)


class App(tk.Tk):
    appconfig = parser['APP']

    def __init__(self, *args, **kwds):
        title = self.appconfig.pop('title')
        super().__init__(*args, **kwds)
        self.title = title
        mixer.init()

        self.geometry = '400x500'
        self.minsize(400, 500)
        self.maxsize(400, 500)

        self.window = Window(self)
        self.front = View(Front(self.window), 'widget')

        self.window.pack(fill='both', expand=True)
        self.window.set_view(self.front)
